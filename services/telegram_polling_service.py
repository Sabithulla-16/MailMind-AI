import requests

from utils.config import (
    TELEGRAM_BOT_TOKEN
)


def get_updates(
    offset=None
):

    url = (
        f"https://api.telegram.org/"
        f"bot{TELEGRAM_BOT_TOKEN}"
        f"/getUpdates"
    )

    params = {}

    if offset:

        params["offset"] = offset

    response = requests.get(
        url,
        params=params
    )

    return response.json()


def send_message(
    chat_id,
    text
):

    url = (
        f"https://api.telegram.org/"
        f"bot{TELEGRAM_BOT_TOKEN}"
        f"/sendMessage"
    )

    requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": text
        }
    )