import json

from services.groq_service import client

from utils.json_parser import (
    parse_json
)

def extract_event(email):

    prompt = f"""
Extract calendar information.

Return JSON only.

Format:

{{
    "has_event": true,
    "event_type": "",
    "title": "",
    "event_date": "",
    "event_time": "",
    "confidence": 0.0
}}

event_date MUST be:

YYYY-MM-DD

Examples:

2026-06-15
2026-07-20

Never return:

15 June 2026
15-Jun-2026
Tomorrow
Next Week

Event Types:

MEETING
INTERVIEW
APPOINTMENT
DEADLINE
BILL

Important Rules:

Do NOT classify newsletters,
promotions,
finance reports,
AI news,
Pinterest,
Reddit,
Duolingo,
marketing emails,
or informational emails
as events.

Only classify as event if:

- meeting
- interview
- appointment
- deadline
- bill due
- scheduled call

Ignore:

- login notifications
- security alerts
- newsletters
- reports
- promotions
- social notifications
- AI news

Only return has_event=true
if a real date or time exists.

If no event exists:

{{
    "has_event": false
}}

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