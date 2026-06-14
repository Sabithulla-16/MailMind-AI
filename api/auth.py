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

        email_address = (
            profile["emailAddress"]
        )

        # ── Resolve or create user ───────────────

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
                    email_address
                )
            )

        if not user:

            user = (
                create_user(
                    email_address
                )
            )

        # Always persist chat_id — whether the user
        # is new or already existed without one.
        if chat_id and not user.get(
            "telegram_chat_id"
        ):

            set_telegram_chat_id(
                user["id"],
                int(chat_id)
            )

        # ── Save Gmail account ───────────────────

        gmail_account = (
            save_gmail_account(
                user_id=user["id"],
                gmail_address=email_address,
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

        # ── Notify Telegram ──────────────────────

        telegram_sent = False
        telegram_error = None

        if chat_id:

            try:

                send_message(
                    (
                        "✅ Gmail Connected!\n\n"
                        f"📧 {email_address}\n\n"
                        "You're all set. Type /help "
                        "to see what I can do."
                    ),
                    int(chat_id),
                )

                telegram_sent = True

            except Exception as e:

                telegram_error = str(e)

                print(
                    f"[auth] Telegram notify "
                    f"failed for chat_id={chat_id}: "
                    f"{telegram_error}"
                )

        # ── Clean up flow store ──────────────────

        flow_store.pop(
            state,
            None
        )

        # ── Success page ─────────────────────────

        telegram_note = (
            "<p>A confirmation has been sent to Telegram.</p>"
            if telegram_sent else
            "<p style='color:#888;font-size:13px'>"
            "Could not send Telegram notification — "
            "but your account is connected. "
            "Return to Telegram and type /help.</p>"
        )

        return HTMLResponse(
            f"""
            <html>
            <head>
                <title>MailMind AI</title>
                <meta name="viewport"
                    content="width=device-width,
                    initial-scale=1">
                <style>
                    body {{
                        font-family: -apple-system,
                            Arial, sans-serif;
                        text-align: center;
                        padding: 80px 24px;
                        background: #f8fafc;
                        color: #1a1a2e;
                    }}
                    .card {{
                        max-width: 400px;
                        margin: 0 auto;
                        background: white;
                        border-radius: 16px;
                        padding: 40px 32px;
                        box-shadow: 0 4px 24px
                            rgba(0,0,0,0.08);
                    }}
                    h1 {{
                        font-size: 22px;
                        margin-bottom: 12px;
                    }}
                    p {{
                        color: #555;
                        line-height: 1.6;
                        margin: 8px 0;
                    }}
                    .email {{
                        font-weight: 600;
                        color: #1a1a2e;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>✅ Gmail Connected!</h1>
                    <p class="email">{email_address}</p>
                    <br>
                    {telegram_note}
                    <p>You may now close this tab
                    and return to Telegram.</p>
                </div>
            </body>
            </html>
            """
        )

    except Exception as e:

        print(f"[auth] google_callback error: {e}")

        return HTMLResponse(
            f"""
            <html>
            <head><title>MailMind AI — Error</title></head>
            <body style="font-family:Arial;
                text-align:center;padding:80px 24px;">
                <h1>❌ Something went wrong</h1>
                <p>{str(e)}</p>
                <p>Please go back to Telegram
                and try /start again.</p>
            </body>
            </html>
            """,
            status_code=500
        )