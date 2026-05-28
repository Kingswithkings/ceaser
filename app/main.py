from fastapi import FastAPI
from app.database.db import Base, engine
from app.routes import auth, chat, goals, profile, insights

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ceaser AI Financial Brain",
    description="AI-powered financial intelligence backend",
    version="0.3.0"
)

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(goals.router)
app.include_router(profile.router)
app.include_router(insights.router)

@app.get("/")
def home():
    return {
        "message": "Ceaser backend is running",
        "version": "0.3.0"
    }