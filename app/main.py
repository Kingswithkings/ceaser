from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.config import load_environment

load_environment()

from app.database.db import Base, engine
from app.routes import auth, chat

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ceaser AI Financial Brain",
    description="AI-powered financial intelligence backend",
    version="0.2.0"
)

cors_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://localhost:5173,http://localhost:5174,"
    "http://127.0.0.1:3000,http://127.0.0.1:5173,http://127.0.0.1:5174",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in cors_origins if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/")
def home():
    return {
        "message": "Ceaser backend is running",
        "version": "0.2.0"
    }
