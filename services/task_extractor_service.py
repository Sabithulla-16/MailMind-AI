import json

from services.groq_service import client

from utils.json_parser import (
    parse_json
)

def extract_task(email):

    prompt = f"""
Extract actionable tasks.

Return JSON only.

Format:

{{
    "has_task": true,
    "task_type": "",
    "title": "",
    "description": "",
    "due_date": "",
    "priority": ""
}}

Only create a task if the user must perform an action.

due_date rules:

Return YYYY-MM-DD only.

Examples:

2026-06-15

If no exact date exists:

return null

Never return:

Soon
Tomorrow
Next Week
2 days from now
No specific due date mentioned
Limited-time application period

Task Types:

PAYMENT
FOLLOW_UP
APPLICATION
ASSIGNMENT
MEETING_PREP
ACTION_REQUIRED

Ignore:

Newsletters
Promotions
Pinterest
Reddit
AI News
Reports
Marketing campaigns
Advertisements
Product launches
Partnership announcements
Informational updates

Subject:
{email.get("subject")}

Summary:
{email.get("detailed_summary")}
"""

    response = (
        client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )
    )

    content = (
        response
        .choices[0]
        .message.content
    )

    content = (
        content
        .replace(
            "```json",
            ""
        )
        .replace(
            "```",
            ""
        )
        .strip()
    )

    return parse_json(content)