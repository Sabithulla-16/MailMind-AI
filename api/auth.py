from fastapi import APIRouter, Request

from fastapi.responses import (
    RedirectResponse,
    HTMLResponse
)

from utils.config import (
    GOOGLE_REDIRECT_URI
)

from services.telegram_service import (
    send_message
)

from services.gmail_service import (
    create_flow,
    get_user_profile
)

from repositories.user_repo import (
    create_user,
    set_telegram_chat_id,
    get_user_by_telegram_chat_id,
    set_active_account,
    get_user_by_email
)

from repositories.gmail_repo import (
    save_gmail_account
)

router = APIRouter(
    prefix="/auth"
)

flow_store = {}


@router.get("/google")
def google_login(
    request: Request,
    chat_id: str = None
):

    flow = create_flow()

    flow.redirect_uri = (
        GOOGLE_REDIRECT_URI
    )

    authorization_url, state = (
        flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent"
        )
    )

    flow_store[state] = {
        "flow": flow,
        "chat_id": chat_id
    }

    return RedirectResponse(
        authorization_url
    )


@router.get("/google/callback")
def google_callback(
    request: Request
):

    state = request.query_params.get(
        "state"
    )

    code = request.query_params.get(
        "code"
    )

    stored = (
        flow_store.get(state)
    )

    if not stored:

        return {
            "success": False,
            "error": "Invalid state"
        }

    flow = stored["flow"]

    chat_id = stored["chat_id"]

    try:

        flow.fetch_token(
            code=code
        )

        credentials = (
            flow.credentials
        )

        profile = (
            get_user_profile(
                credentials
            )
        )

        user = None

        if chat_id:

            user = (
                get_user_by_telegram_chat_id(
                    int(chat_id)
                )
            )

        if not user:

            user = (
                get_user_by_email(
                    profile[
                        "emailAddress"
                    ]
                )
            )

        if not user:

            user = (
                create_user(
                    profile[
                        "emailAddress"
                    ]
                )
            )

            if chat_id:

                set_telegram_chat_id(
                    user["id"],
                    int(chat_id)
                )

        gmail_account = (
            save_gmail_account(
                user_id=user["id"],
                gmail_address=profile[
                    "emailAddress"
                ],
                access_token=credentials.token,
                refresh_token=credentials.refresh_token
            )
        )

        if not user.get(
            "active_gmail_account_id"
        ):

            set_active_account(
                user["id"],
                gmail_account["id"]
            )

        if chat_id:

            try:

                send_message(
                    int(chat_id),
                    (
                        "✅ Gmail Connected Successfully\n\n"
                        f"📧 {profile['emailAddress']}\n\n"
                        "You may now start using MailMind AI!"
                    )
                )

            except Exception as e:

                print(
                    f"Telegram notify failed: {e}"
                )

        flow_store.pop(
            state,
            None
        )

        return HTMLResponse(
            """
            <html>
            <head>
                <title>MailMind AI</title>
            </head>

            <body style="
                font-family: Arial;
                text-align: center;
                padding-top: 100px;
                background-color: #f8fafc;
            ">

                <h1>
                    ✅ Gmail Connected Successfully
                </h1>

                <p>
                    Your Gmail account has been
                    linked to MailMind AI.
                </p>

                <p>
                    A confirmation message has
                    been sent to Telegram.
                </p>

                <p>
                    You may now close this tab
                    and return to Telegram.
                </p>

            </body>
            </html>
            """
        )

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }