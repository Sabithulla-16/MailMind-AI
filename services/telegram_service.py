import requests

from utils.config import (
    TELEGRAM_BOT_TOKEN
)


def send_message(
    chat_id: int,
    text: str
):

    url = (
        f"https://api.telegram.org"
        f"/bot{TELEGRAM_BOT_TOKEN}"
        f"/sendMessage"
    )

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    response = requests.post(
        url,
        json=payload,
        timeout=10
    )

    if not response.ok:

        raise RuntimeError(
            f"Telegram API error "
            f"{response.status_code}: "
            f"{response.text}"
        )

    return response.json()