from repositories.gmail_repo import (
    get_all_gmail_accounts
)


def get_google_account():

    accounts = (
        get_all_gmail_accounts()
    )

    if not accounts:
        return None

    return accounts[0]