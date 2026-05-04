from pathlib import Path
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing. Create .env beside main.py.")

print("ENV FILE:", ENV_PATH)
print("LOADED KEY STARTS WITH:", api_key[:12])

client = OpenAI(api_key=api_key)

app = FastAPI(title="Ceaser Backend")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "Ceaser backend is running"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "env_file_exists": ENV_PATH.exists(),
        "api_key_loaded": bool(api_key),
        "api_key_starts_with": api_key[:12],
    }


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Ceaser, an AI financial brain. "
                        "Help users understand spending, budgeting, bills, savings, "
                        "financial goals, and money decisions clearly."
                    ),
                },
                {
                    "role": "user",
                    "content": request.message,
                },
            ],
        )

        return {
            "reply": response.choices[0].message.content
        }

    except Exception as e:
        print("CHAT ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))