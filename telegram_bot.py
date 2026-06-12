from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

from telegram.constants import (
    ChatAction
)

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from utils.config import (
    TELEGRAM_BOT_TOKEN,
    BACKEND_URL
)

from agents.telegram_command_agent import (
    TelegramCommandAgent
)


agent = TelegramCommandAgent()


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        text = (
            update.message.text
            or ""
        )

        chat_id = (
            update.effective_chat.id
        )

        if text == "/start":

            url = (
                f"{BACKEND_URL}"
                f"/auth/google"
                f"?chat_id={chat_id}"
            )

            keyboard = [
                [
                    InlineKeyboardButton(
                        "🔗 Connect Gmail",
                        url=url
                    )
                ]
            ]

            reply_markup = (
                InlineKeyboardMarkup(
                    keyboard
                )
            )

            await update.message.reply_text(
                "👋 Welcome to MailMind AI\n\n"
                "Connect your Gmail account:",
                reply_markup=reply_markup
            )

            return

        print(
            update.effective_chat.id
        )

        await context.bot.send_chat_action(
            chat_id=chat_id,
            action=ChatAction.TYPING
        )

        response = (
            agent.handle(
                text,
                chat_id
            )
        )

        await update.message.reply_text(
            response[:4000],
            parse_mode="HTML"
        )

    except Exception as e:

        await update.message.reply_text(
            f"Error:\n{str(e)}"
        )


def main():

    app = (
        ApplicationBuilder()
        .token(
            TELEGRAM_BOT_TOKEN
        )
        .build()
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND,
            handle_message
        )
    )

    app.add_handler(
        MessageHandler(
            filters.COMMAND,
            handle_message
        )
    )

    print(
        "Telegram Bot Running..."
    )

    app.run_polling()


if __name__ == "__main__":

    main()