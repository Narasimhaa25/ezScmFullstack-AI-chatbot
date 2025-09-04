from fastapi import APIRouter, Query, Depends, HTTPException
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.models import Message, Session as ChatSession
from app.services.ai_providers import openai_stream, anthropic_stream, gemini_stream
import uuid
import json
from uuid import UUID

router = APIRouter()

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------
# Sessions & Messages Routes
# ---------------------------

@router.get("/sessions")
def get_sessions(db: Session = Depends(get_db)):
    sessions = db.query(ChatSession).all()
    return [{"id": str(s.id), "title": s.title or "Untitled"} for s in sessions]

@router.get("/messages/{session_id}")
def get_messages(session_id: UUID, db: Session = Depends(get_db)):
    messages = db.query(Message).filter_by(session_id=session_id).all()
    return [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "provider": m.provider,
            "model": m.model
        }
        for m in messages
    ]

# ---------------------------
# Streaming Chat Route
# ---------------------------

@router.get("/stream")
async def stream_chat(
    session_id: str = Query(..., description="UUID of session"),
    provider: str = Query("gemini", description="AI provider: openai, claude, gemini"),
    model: str = Query("default", description="Provider-specific model selection"),
    prompt: str = Query(..., description="User input prompt"),
    db: Session = Depends(get_db),
):
    async def event_generator():
        # Validate UUID
        try:
            session_uuid = uuid.UUID(session_id)
        except ValueError:
            yield json.dumps({"delta": "Invalid session_id"})
            return

        # Ensure session exists
        session_obj = db.query(ChatSession).filter_by(id=session_uuid).first()
        if not session_obj:
            session_obj = ChatSession(id=session_uuid, title="New Session")
            db.add(session_obj)
            db.commit()

        # Save user message
        user_message = Message(
            session_id=session_uuid,
            role="user",
            content=prompt,
            provider="user",
            model="",
        )
        db.add(user_message)
        db.commit()

        # Select AI provider
        provider_lower = provider.lower()
        if provider_lower == "openai":
            stream_func = lambda p: openai_stream(p, model=model)
        elif provider_lower == "claude":
            stream_func = lambda p: anthropic_stream(p, model=model)
        elif provider_lower == "gemini":
            # Gemini only uses default flash model internally
            stream_func = lambda p: gemini_stream(p)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported provider '{provider}'")

        assistant_message = ""

        # Stream AI response token by token
        async for token in stream_func(prompt):
            assistant_message += token
            yield json.dumps({"delta": token})

        # Save final assistant message
        db_message = Message(
            session_id=session_uuid,
            role="assistant",
            content=assistant_message,
            provider=provider_lower,
            model=model,
        )
        db.add(db_message)
        db.commit()

        # End of stream
        yield json.dumps({"delta": "[DONE]"})

    return EventSourceResponse(event_generator())