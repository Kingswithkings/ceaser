from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterRequest(BaseModel):
    full_name: Optional[str] = None
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class GoalCreate(BaseModel):
    title: str
    target_amount: Optional[int] = None

class UserProfileCreate(BaseModel):
    income_type: Optional[str] = None
    financial_goal: Optional[str] = None
    risk_level: Optional[str] = None
    country: Optional[str] = "UK"
    financial_knowledge: Optional[str] = None