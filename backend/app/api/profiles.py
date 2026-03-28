from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import UserProfile
from app.schemas.schemas import UserProfileUpdate

router = APIRouter()

@router.put("/{user_id}")
async def update_profile(
    user_id: int,
    profile_update: UserProfileUpdate,
    db: Session = Depends(get_db)
):
    """Update user profile and interests"""
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields
    if profile_update.name:
        user.name = profile_update.name
    if profile_update.profile_type:
        user.profile_type = profile_update.profile_type
    if profile_update.interests:
        user.interests = profile_update.interests
    if profile_update.preferences:
        user.preferences = profile_update.preferences
    
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "profile_type": user.profile_type,
        "interests": user.interests,
        "preferences": user.preferences
    }

@router.post("/{user_id}/interests")
async def add_interests(
    user_id: int,
    interests: dict,
    db: Session = Depends(get_db)
):
    """Add interests to user profile"""
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.interests:
        user.interests = {}
    
    # Merge interests
    for key, value in interests.items():
        if key not in user.interests:
            user.interests[key] = []
        user.interests[key].extend(value)
        user.interests[key] = list(set(user.interests[key]))  # Remove duplicates
    
    db.commit()
    db.refresh(user)
    
    return {"interests": user.interests}
