from database.supabase import supabase

def save_gmail_account(
    user_id,
    gmail_address,
    access_token,
    refresh_token
):

    result = (
        supabase
        .table("gmail_accounts")
        .upsert(
            {
                "user_id": user_id,
                "gmail_address": gmail_address,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "connected": True
            }
        )
        .execute()
    )

    return result.data[0]

from database.supabase import supabase


def get_all_gmail_accounts():

    result = (
        supabase
        .table("gmail_accounts")
        .select("*")
        .eq("connected", True)
        .execute()
    )

    return result.data


def get_gmail_account(email):

    result = (
        supabase
        .table("gmail_accounts")
        .select("*")
        .eq("gmail_address", email)
        .execute()
    )

    return result.data

def get_user_accounts(
    user_id
):

    result = (
        supabase
        .table("gmail_accounts")
        .select("*")
        .eq(
            "user_id",
            user_id
        )
        .execute()
    )

    return result.data

def get_account_by_email(
    email
):

    result = (
        supabase
        .table("gmail_accounts")
        .select("*")
        .eq(
            "gmail_address",
            email
        )
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]

def get_account_by_id(
    account_id
):

    result = (
        supabase
        .table("gmail_accounts")
        .select("*")
        .eq(
            "id",
            account_id
        )
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]