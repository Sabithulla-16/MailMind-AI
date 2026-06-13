import json

from services.groq_service import client

from utils.json_parser import (
    parse_json
)

def extract_event(email):

    prompt = f"""
TASK: Determine if the email contains a real calendar event and extract it.

═══════════════════════════════════════
ABSOLUTE OUTPUT RULES (never violate):
═══════════════════════════════════════
1. Output MUST start with {{ and end with }}
2. No markdown. No code fences. No preamble. No explanation.
3. NEVER invent a date, time, or event title not explicitly stated in the email.
4. NEVER interpret relative terms like "tomorrow", "next week", "soon" as real dates.
5. If no real event exists → return the NO-EVENT object below. Nothing else.

══════════════════════════════════════════════════
OUTPUT SCHEMA — When a real event IS found:
══════════════════════════════════════════════════
{{
    "has_event": true,
    "event_type": "<see EVENT TYPE RULES>",
    "title": "<short descriptive title>",
    "event_date": "<YYYY-MM-DD>",
    "event_time": "<HH:MM in 24h format, or null if not stated>",
    "confidence": <float 0.0 to 1.0>
}}

══════════════════════════════════════════════════
OUTPUT SCHEMA — When NO real event is found:
══════════════════════════════════════════════════
{{
    "has_event": false
}}

═══════════════════════
EVENT DATE FORMAT RULE:
═══════════════════════
event_date MUST always be: YYYY-MM-DD

✓ CORRECT:  "2026-06-15"
✗ WRONG:    "15 June 2026"
✗ WRONG:    "15-Jun-2026"
✗ WRONG:    "Tomorrow"
✗ WRONG:    "Next Monday"
✗ WRONG:    "In 2 days"

If only a relative date exists (tomorrow, next week) → has_event: false

═══════════════════
EVENT TYPE RULES:
═══════════════════
MEETING     → scheduled call, video call, team meeting, sync, standup
INTERVIEW   → job interview, hiring call, candidate screening
APPOINTMENT → doctor, dentist, service booking, personal appointment
DEADLINE    → task due date, submission deadline, application close date
BILL        → payment due date, invoice due, subscription renewal date

══════════════════════════════════════════════
EMAILS THAT MUST ALWAYS RETURN has_event: false
══════════════════════════════════════════════
These email types NEVER contain calendar events:
  ✗ Newsletters and digests
  ✗ Promotional and marketing emails
  ✗ Finance reports or portfolio updates
  ✗ AI news and product announcements
  ✗ Social media notifications (Pinterest, Reddit, LinkedIn likes)
  ✗ Login alerts and security notifications
  ✗ Informational updates with no scheduled action
  ✗ Gamification emails (Duolingo streaks, app activity)
  ✗ Shipping or order updates (unless a delivery appointment exists)

RULE: Only return has_event: true if a SPECIFIC date (YYYY-MM-DD) can be extracted.
RULE: The event must contain a specific actionable date.
This includes meetings, interviews, appointments,
deadlines, due dates, renewal dates, and payment dates.
═══════════════
EMAIL DATA:
═══════════════
Subject: {email.get("subject")}
Summary: {email.get("detailed_summary")}

Now output the JSON object. Start with {{ and end with }}.
"""

    response = (
        client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a JSON-only calendar event extractor. You output one valid JSON object. Nothing else."
                },
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