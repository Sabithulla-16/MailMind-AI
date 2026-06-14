from googleapiclient.discovery import build

from google.oauth2.credentials import (
    Credentials
)

def get_tasks_service(
    access_token,
    refresh_token
):

    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token
    )

    return build(
        "tasks",
        "v1",
        credentials=creds
    )