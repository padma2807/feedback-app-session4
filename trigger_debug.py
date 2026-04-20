import os
import httpx
import asyncio
from dotenv import load_dotenv

# Path to the .env file in the backend folder
dotenv_path = os.path.join('backend', '.env')
load_dotenv(dotenv_path)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def test_telegram_notification():
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID or TELEGRAM_BOT_TOKEN == "your_bot_token_here":
        print("❌ Telegram configuration missing or placeholder. Please update backend/.env")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    message = "🧪 *Feedback App Test Notification*\nYour Telegram integration is working correctly!"
    
    print(f"Attempting to send message to Chat ID: {TELEGRAM_CHAT_ID}...")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            })
            if response.status_code == 200:
                print("✅ Test message sent successfully!")
            else:
                print(f"❌ Failed to send message. Status: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"❌ Error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(test_telegram_notification())
