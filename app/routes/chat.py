from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from openai import OpenAI
import os

from app.config import load_environment
from app.database.db import get_db
from app.models.models import User, Conversation, Message
from app.schemas.schemas import ChatRequest
from app.auth.security import get_current_user

load_environment()

router = APIRouter(prefix="/chat", tags=["AI Chat"])

SYSTEM_PROMPT = """
You are Ceaser, an AI financial intelligence assistant.

You help users understand, organise, and improve their financial decisions.
You provide educational financial guidance, not regulated financial advice.

You help with budgeting, saving, debt reduction, goal tracking, spending habits,
financial education, income planning, and disciplined decision-making.

You must not promise guaranteed financial outcomes.
"""

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured")
    return OpenAI(api_key=api_key)

@router.post("/")
def chat(
    data: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if data.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == data.conversation_id,
            Conversation.user_id == current_user.id
        ).first()
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(
            title=data.message[:50],
            user_id=current_user.id
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    user_message = Message(
        role="user",
        content=data.message,
        conversation_id=conversation.id
    )
    db.add(user_message)
    db.commit()

    previous_messages = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at.asc()).all()

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in previous_messages[-20:]:
        messages.append({
            "role": msg.role,
            "content": msg.content
        })

    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    reply = response.choices[0].message.content

    assistant_message = Message(
        role="assistant",
        content=reply,
        conversation_id=conversation.id
    )

    db.add(assistant_message)
    db.commit()

    return {
        "conversation_id": conversation.id,
        "reply": reply
    }

@router.get("/history")
def history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).order_by(Conversation.created_at.desc()).all()

    return conversations
