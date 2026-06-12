import threading
import uvicorn
import os

print("1")

from scheduler import (
    start_scheduler
)

print("2")

from telegram_bot import (
    main as telegram_main
)

print("3")


def run_scheduler():

    print(
        "scheduler thread"
    )

    start_scheduler()


def run_telegram():

    print(
        "telegram thread"
    )

    telegram_main()


if __name__ == "__main__":

    threading.Thread(
        target=run_scheduler,
        daemon=True
    ).start()

    print("4")

    threading.Thread(
        target=run_telegram,
        daemon=True
    ).start()

    print("5")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                8000
            )
        )
    )