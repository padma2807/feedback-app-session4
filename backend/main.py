import os
import httpx
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from database import engine, Base, get_db
from models import Feedback, FeedbackCreate

# Load environment variables
load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Feedback Masai Live API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_telegram_message(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram configuration missing. Skipping message.")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            })
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending Telegram message: {e}")
            return False

@app.post("/submit-feedback")
async def submit_feedback(data: FeedbackCreate, db: Session = Depends(get_db)):
    # Save to Database
    new_feedback = Feedback(
        name=data.name,
        email=data.email,
        rating=data.rating,
        experience=data.experience
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    # Prepare Telegram Message
    msg = (
        "🚀 *New Feedback Received:*\n\n"
        f"👤 *Name:* {data.name}\n"
        f"📧 *Email:* {data.email}\n"
        f"⭐ *Rating:* {'⭐' * data.rating}\n\n"
        f"📝 *Experience:* \n{data.experience}"
    )

    # Send Notification
    await send_telegram_message(msg)

    return {"message": "Feedback submitted successfully!", "id": new_feedback.id}

@app.get("/health")
def health_check():
    return {"status": "ok"}
