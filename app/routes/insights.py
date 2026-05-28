from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from openai import OpenAI
import os
from dotenv import load_dotenv

from app.database.db import get_db
from app.models.models import User, Goal, UserProfile, Message
from app.auth.security import get_current_user

load_dotenv()

router = APIRouter(prefix="/insights", tags=["AI Insights"])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.get("/daily")
def daily_insight(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()

    goals = db.query(Goal).filter(
        Goal.user_id == current_user.id
    ).all()

    recent_messages = db.query(Message).order_by(
        Message.created_at.desc()
    ).limit(10).all()

    prompt = f"""
    Create one short daily financial insight for this user.

    User profile:
    {profile}

    User goals:
    {goals}

    Recent financial conversations:
    {recent_messages}

    Keep it practical, motivational, and educational.
    Do not provide regulated financial advice.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are Ceaser, an AI financial intelligence assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "daily_insight": response.choices[0].message.content
    }