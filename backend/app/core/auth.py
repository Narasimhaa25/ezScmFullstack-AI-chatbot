from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.models import User
from datetime import datetime
import uuid

router = APIRouter()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(email: str, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.email == email).first()

    if not user:
        # Auto-register if not found
        user = User(
            id=uuid.uuid4(),
            username=email.split("@")[0],
            email=email,
            created_at=datetime.utcnow(),
            last_login=datetime.utcnow()
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    else:
        # Update last login if user exists
        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)

    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at,
        "last_login": user.last_login
    }