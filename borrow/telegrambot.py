import os

import requests
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")


def send_notification(message):
    requests.get(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        {"chat_id": chat_id, "text": message},
    )
