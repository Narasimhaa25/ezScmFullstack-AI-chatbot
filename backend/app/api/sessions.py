from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine, Base
from app.models import Session as SessionModel, Message
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/sessions", tags=["sessions"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------
# Get all sessions
# -----------------------
@router.get("/")
def get_sessions(db: Session = Depends(get_db)):
    sessions = db.query(SessionModel).order_by(SessionModel.updated_at.desc()).all()
    return sessions

# -----------------------
# Create new session
# -----------------------
@router.post("/")
def create_session(db: Session = Depends(get_db)):
    new_session = SessionModel(
        id=uuid.uuid4(),
        title="New Chat",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        provider="gemini",
        model="gemini-pro"
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

# -----------------------
# Get messages for a session
# -----------------------
@router.get("/{session_id}/messages")
def get_messages(session_id: str, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.session_id == session_id).all()
    if messages is None or len(messages) == 0:
        raise HTTPException(status_code=404, detail="Session not found or no messages")
    return messages