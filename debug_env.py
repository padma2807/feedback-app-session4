import os
from dotenv import load_dotenv

# Path to the .env file in the backend folder
dotenv_path = os.path.join('backend', '.env')
load_dotenv(dotenv_path)

def check_env():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    print("--- Environment Variable Check ---")
    if token and token != "your_bot_token_here":
        print(f"✅ TELEGRAM_BOT_TOKEN: Found (Starts with {token[:5]}...)")
    else:
        print("❌ TELEGRAM_BOT_TOKEN: Missing or placeholder")
        
    if chat_id and chat_id != "your_chat_id_here":
        print(f"✅ TELEGRAM_CHAT_ID: Found ({chat_id})")
    else:
        print("❌ TELEGRAM_CHAT_ID: Missing or placeholder")
    print("----------------------------------")

if __name__ == "__main__":
    check_env()
