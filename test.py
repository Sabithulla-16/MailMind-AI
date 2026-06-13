# test_digest_command.py

import json

from repositories.digest_repo import (
    get_latest_digest_by_account
)

ACCOUNT_ID = (
    "5b7edad3-8949-4867-8be0-82343f841c27"
)

digest = (
    get_latest_digest_by_account(
        ACCOUNT_ID
    )
)

print("RAW:")
print(digest)

print("\nTYPE:")
print(
    type(
        digest["digest_text"]
    )
)

digest_data = json.loads(
    digest["digest_text"]
)

message = (
    "🧠 Latest AI Digest\n\n"
    + digest_data.get(
        "header",
        ""
    )
)

for category, items in (
    digest_data.get(
        "by_category",
        {}
    ).items()
):

    message += (
        f"\n\n📂 {category}"
    )

    for item in items:

        message += (
            f"\n• {item}"
        )

if digest_data.get(
    "action_required"
):

    message += (
        "\n\n⚠ Action Required"
    )

    for item in digest_data[
        "action_required"
    ]:

        message += (
            f"\n• {item}"
        )

print("\n\nFINAL MESSAGE:\n")
print(message)