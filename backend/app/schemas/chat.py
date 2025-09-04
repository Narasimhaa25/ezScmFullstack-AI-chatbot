from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class MessageCreate(BaseModel):
    session_id: UUID
    role: str  # 'user' or 'assistant'
    content: str
    provider: Optional[str] = None
    model: Optional[str] = None
    tokens_used: Optional[int] = 0

class SessionCreate(BaseModel):
    user_id: UUID
    title: str
    provider: str
    model: str