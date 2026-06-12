import requests

from utils.config import (
    TELEGRAM_BOT_TOKEN
)


def send_message(
    text,
    chat_id):

    url = (
        f"https://api.telegram.org/"
        f"bot{TELEGRAM_BOT_TOKEN}"
        f"/sendMessage"
    )

    payload = {
        "chat_id":
            chat_id,

        "text":
            text
    }

    response = requests.post(
        url,
        json=payload
    )

    return response.json()