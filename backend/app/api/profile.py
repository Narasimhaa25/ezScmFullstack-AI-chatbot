# profile.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db  # your database session dependency
from models import User      # your User SQLAlchemy model
from dependencies import get_current_user  # your auth dependency

router = APIRouter(prefix="/api", tags=["Profile"])

@router.get("/profile")
def get_profile(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Get the currently authenticated user's profile.
    """
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    # Optionally, fetch fresh data from DB
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }