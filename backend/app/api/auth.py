from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import UserProfile, UserSession
from app.schemas.schemas import UserProfileCreate, UserProfileUpdate
from datetime import datetime, timedelta
import uuid
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email: str

@router.post("/signup")
async def signup(user_data: UserProfileCreate, db: Session = Depends(get_db)):
    """Register a new user with profile type"""
    try:
        # Check if user exists
        existing_user = db.query(UserProfile).filter(UserProfile.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        user = UserProfile(
            email=user_data.email,
            name=user_data.name,
            profile_type=user_data.profile_type,
            interests=user_data.interests
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create session token
        token = str(uuid.uuid4())
        session = UserSession(
            user_id=user.id,
            token=token,
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        db.add(session)
        db.commit()
        
        return {
            "user_id": user.id,
            "email": user.email,
            "name": user.name,
            "profile_type": user.profile_type,
            "token": token
        }
    except Exception as e:
        print(f"SIGNUP ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Signup error: {str(e)}")

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login user (simplified for MVP)"""
    user = db.query(UserProfile).filter(UserProfile.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    token = str(uuid.uuid4())
    session = UserSession(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(days=30)
    )
    db.add(session)
    db.commit()
    
    return {
        "user_id": user.id,
        "email": user.email,
        "token": token
    }

@router.get("/profile/{user_id}")
async def get_profile(user_id: int, db: Session = Depends(get_db)):
    """Get user profile"""
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "profile_type": user.profile_type,
        "interests": user.interests,
        "preferences": user.preferences
    }
