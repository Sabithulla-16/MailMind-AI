from fastapi import APIRouter, Request

from utils.config import GOOGLE_REDIRECT_URI

from fastapi.responses import RedirectResponse

from services.gmail_service import (
    create_flow,
    get_user_profile,
    fetch_recent_emails,
    get_email_details,
    parse_email
)

from repositories.user_repo import (
    create_user,
    set_telegram_chat_id,
    get_user_by_telegram_chat_id
)

from repositories.user_repo import (
    set_active_account
)

from repositories.user_repo import (
    get_user_by_email
)

from repositories.gmail_repo import save_gmail_account

router = APIRouter(prefix="/auth")

flow_store = {}


@router.get("/google")
def google_login(
    request: Request,
    chat_id: str = None
):

    flow = create_flow()

    flow.redirect_uri = GOOGLE_REDIRECT_URI

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )

    flow_store[state] = flow

    request.session[
        "telegram_chat_id"
    ] = chat_id

    return RedirectResponse(
        authorization_url
    )


@router.get("/google/callback")
def google_callback(
    request: Request,
    chat_id: str = None
):

    state = request.query_params.get("state")
    code = request.query_params.get("code")

    flow = flow_store.get(state)

    if not flow:
        return {
            "success": False,
            "error": "Invalid state"
        }

    try:

        flow.fetch_token(code=code)

        credentials = flow.credentials

        profile = get_user_profile(
            credentials
        )

        chat_id = (
            request.session.get(
                "telegram_chat_id"
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
                    profile["emailAddress"]
                )
            )

        if not user:

            user = (
                create_user(
                    profile["emailAddress"]
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
                gmail_address=profile["emailAddress"],
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

        return {
            "success": True,
            "email": profile.get("emailAddress"),
            "messages_total": profile.get("messagesTotal"),
            "threads_total": profile.get("threadsTotal")
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }