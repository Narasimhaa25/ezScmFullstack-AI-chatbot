from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.api import sessions
from fastapi import HTTPException, status
from app.core.config import SessionLocal, engine, Base
from app.models import User
from app.api import chat, auth  # ✅ import routers

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Chatbot Backend")

# CORS setup (React frontend)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(sessions.router)

# Dependency: DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Debug/Test route (see all registered users)
@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# Dependency to get a current user (for demo, we pick the first user)
def get_current_user(db: Session = Depends(get_db)):
    user = db.query(User).first()  # Replace with proper auth logic if available
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No user found"
        )
    return user

# Profile endpoint
@app.get("/api/profile")
def read_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at,
        "last_login": current_user.last_login
    }