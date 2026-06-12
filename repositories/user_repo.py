from database.supabase import (
    supabase
)


def create_user(
    email
):

    result = (
        supabase
        .table("users")
        .upsert(
            {
                "email": email
            }
        )
        .execute()
    )

    return result.data[0]


def get_user_by_email(
    email
):

    result = (
        supabase
        .table("users")
        .select("*")
        .eq(
            "email",
            email
        )
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]

def set_active_account(
    user_id,
    gmail_account_id
):

    return (
        supabase
        .table("users")
        .update(
            {
                "active_gmail_account_id":
                    gmail_account_id
            }
        )
        .eq(
            "id",
            user_id
        )
        .execute()
    )

def get_active_account(
    user_id
):

    result = (
        supabase
        .table("users")
        .select(
            "active_gmail_account_id"
        )
        .eq(
            "id",
            user_id
        )
        .execute()
    )

    return result.data[0]

def get_user_by_id(
    user_id
):

    result = (
        supabase
        .table("users")
        .select("*")
        .eq(
            "id",
            user_id
        )
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]

def get_active_account_id(
    user_id
):

    result = (
        supabase
        .table("users")
        .select(
            "active_gmail_account_id"
        )
        .eq(
            "id",
            user_id
        )
        .execute()
    )

    if not result.data:
        return None

    return result.data[0][
        "active_gmail_account_id"
    ]

def get_first_user():

    result = (
        supabase
        .table("users")
        .select("*")
        .limit(1)
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]

def get_user_by_telegram_chat_id(
    chat_id
):

    result = (
        supabase
        .table("users")
        .select("*")
        .eq(
            "telegram_chat_id",
            chat_id
        )
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]

def set_telegram_chat_id(
    user_id,
    chat_id
):

    return (
        supabase
        .table("users")
        .update(
            {
                "telegram_chat_id":
                    chat_id
            }
        )
        .eq(
            "id",
            user_id
        )
        .execute()
    )