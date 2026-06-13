from repositories.gmail_repo import (
    get_account_by_id
)


def get_google_account(
    gmail_account_id
):

    return (
        get_account_by_id(
            gmail_account_id
        )
    )