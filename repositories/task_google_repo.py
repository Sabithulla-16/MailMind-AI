from database.supabase import (
    supabase
)

def get_google_account(
    gmail_account_id
):

    result = (
        supabase
        .table(
            "gmail_accounts"
        )
        .select("*")
        .eq(
            "id",
            gmail_account_id
        )
        .limit(1)
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]