from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import User
from app.core.config import SessionLocal

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dummy current user (replace with JWT/auth logic later)
def get_current_user(db: Session = Depends(get_db)) -> User:
    # For testing, we just return the first user in DB
    user = db.query(User).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authenticated user found",
        )
    return user