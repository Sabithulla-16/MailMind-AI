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
                        "✓ Gmail Connected!\n\n"
                        f"◉ {email_address}\n\n"
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
            "<p class='tg-note sent'>✓ Confirmation sent to Telegram.</p>"
            if telegram_sent else
            "<p class='tg-note'>"
            "Could not reach Telegram — "
            "but your account is connected. "
            "Return to Telegram and type /help.</p>"
        )

        return HTMLResponse(
            f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MailMind AI</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #0b0f1a;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      padding: 24px;
    }}
    .card {{
      width: 100%;
      max-width: 420px;
      background: #111827;
      border: 1px solid rgba(255,255,255,0.07);
      border-radius: 24px;
      padding: 48px 40px 40px;
      text-align: center;
      box-shadow:
        0 0 0 1px rgba(255,255,255,0.03),
        0 32px 64px rgba(0,0,0,0.5),
        0 0 80px rgba(79,172,254,0.04);
      animation: rise 0.5s cubic-bezier(0.22,1,0.36,1) both;
    }}
    @keyframes rise {{
      from {{ opacity: 0; transform: translateY(20px); }}
      to   {{ opacity: 1; transform: translateY(0); }}
    }}
    .icon-ring {{
      width: 72px;
      height: 72px;
      margin: 0 auto 28px;
      border-radius: 50%;
      background: linear-gradient(135deg, #1a2a3a 0%, #0f1e2e 100%);
      border: 1px solid rgba(79,172,254,0.25);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 32px rgba(79,172,254,0.12);
    }}
    .checkmark {{
      width: 32px;
      height: 32px;
      stroke: #4facfe;
      stroke-width: 2.5;
      stroke-linecap: round;
      stroke-linejoin: round;
      fill: none;
      stroke-dasharray: 60;
      stroke-dashoffset: 60;
      animation: draw 0.6s 0.3s ease forwards;
    }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    .brand {{
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: #4facfe;
      margin-bottom: 12px;
    }}
    h1 {{
      font-size: 24px;
      font-weight: 700;
      color: #f0f4ff;
      letter-spacing: -0.5px;
      margin-bottom: 8px;
    }}
    .subtitle {{
      font-size: 14px;
      color: rgba(255,255,255,0.4);
      margin-bottom: 28px;
    }}
    .email-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(79,172,254,0.08);
      border: 1px solid rgba(79,172,254,0.18);
      border-radius: 100px;
      padding: 8px 18px;
      font-size: 13px;
      font-weight: 500;
      color: #a8c8fe;
      margin-bottom: 28px;
      word-break: break-all;
    }}
    .email-dot {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #4facfe;
      flex-shrink: 0;
      box-shadow: 0 0 6px #4facfe;
    }}
    .divider {{
      border: none;
      border-top: 1px solid rgba(255,255,255,0.06);
      margin: 0 0 24px;
    }}
    .tg-note {{
      font-size: 13px;
      color: rgba(255,255,255,0.25);
      margin-bottom: 20px;
      line-height: 1.6;
    }}
    .tg-note.sent {{
      color: rgba(86,212,133,0.7);
    }}
    .close-hint {{
      font-size: 12px;
      color: rgba(255,255,255,0.18);
      letter-spacing: 0.3px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="icon-ring">
      <svg class="checkmark" viewBox="0 0 32 32">
        <polyline points="6,17 13,24 26,9"/>
      </svg>
    </div>
    <p class="brand">MailMind AI</p>
    <h1>Gmail Connected</h1>
    <p class="subtitle">Your account is linked and ready.</p>
    <div class="email-badge">
      <span class="email-dot"></span>
      {email_address}
    </div>
    <hr class="divider">
    {telegram_note}
    <p class="close-hint">You may close this tab and return to Telegram.</p>
  </div>
</body>
</html>"""
        )

    except Exception as e:

        print(f"[auth] google_callback error: {e}")

        return HTMLResponse(
            f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MailMind AI — Error</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #0b0f1a;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      padding: 24px;
    }}
    .card {{
      width: 100%;
      max-width: 420px;
      background: #111827;
      border: 1px solid rgba(255,80,80,0.12);
      border-radius: 24px;
      padding: 48px 40px 40px;
      text-align: center;
      box-shadow: 0 32px 64px rgba(0,0,0,0.5);
      animation: rise 0.5s cubic-bezier(0.22,1,0.36,1) both;
    }}
    @keyframes rise {{
      from {{ opacity: 0; transform: translateY(20px); }}
      to   {{ opacity: 1; transform: translateY(0); }}
    }}
    .icon-ring {{
      width: 72px;
      height: 72px;
      margin: 0 auto 28px;
      border-radius: 50%;
      background: rgba(255,80,80,0.07);
      border: 1px solid rgba(255,80,80,0.2);
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .x-mark {{
      width: 28px;
      height: 28px;
      stroke: #ff6b6b;
      stroke-width: 2.5;
      stroke-linecap: round;
      fill: none;
      stroke-dasharray: 50;
      stroke-dashoffset: 50;
      animation: draw 0.5s 0.3s ease forwards;
    }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    .brand {{
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: #ff6b6b;
      margin-bottom: 12px;
    }}
    h1 {{
      font-size: 22px;
      font-weight: 700;
      color: #f0f4ff;
      letter-spacing: -0.5px;
      margin-bottom: 8px;
    }}
    .msg {{
      font-size: 13px;
      color: rgba(255,255,255,0.35);
      margin-bottom: 24px;
      line-height: 1.6;
    }}
    .hint {{
      font-size: 12px;
      color: rgba(255,255,255,0.2);
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="icon-ring">
      <svg class="x-mark" viewBox="0 0 28 28">
        <line x1="6" y1="6" x2="22" y2="22"/>
        <line x1="22" y1="6" x2="6" y2="22"/>
      </svg>
    </div>
    <p class="brand">MailMind AI</p>
    <h1>Something went wrong</h1>
    <p class="msg">{str(e)}</p>
    <p class="hint">Return to Telegram and type /start to try again.</p>
  </div>
</body>
</html>""",
            status_code=500
        )