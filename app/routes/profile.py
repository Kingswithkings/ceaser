from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import User, UserProfile
from app.schemas.schemas import UserProfileCreate
from app.auth.security import get_current_user

router = APIRouter(prefix="/profile", tags=["User Profile"])

@router.post("/onboarding")
def save_onboarding(
    data: UserProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()

    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    profile.income_type = data.income_type
    profile.financial_goal = data.financial_goal
    profile.risk_level = data.risk_level
    profile.country = data.country
    profile.financial_knowledge = data.financial_knowledge

    db.commit()
    db.refresh(profile)

    return {
        "message": "Profile saved successfully",
        "profile": {
            "income_type": profile.income_type,
            "financial_goal": profile.financial_goal,
            "risk_level": profile.risk_level,
            "country": profile.country,
            "financial_knowledge": profile.financial_knowledge
        }
    }


@router.get("/")
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()

    return {
        "user": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email
        },
        "profile": profile
    }