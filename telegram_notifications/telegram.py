import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send_telegram_message(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("Telegram credentials are not set")

    data = {
        "chat_id": CHAT_ID,
        "text": message,
    }

    print(f"==> Sending message to Telegram:\n{data}\nURL: {TELEGRAM_API_URL}")
    response = requests.post(TELEGRAM_API_URL, data=data)

    print(f"==> Telegram response:\nStatus code: {response.status_code}\nText: {response.text}")
    response.raise_for_status()
