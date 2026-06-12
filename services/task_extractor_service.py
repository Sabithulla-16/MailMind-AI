import json

from services.groq_service import client

from utils.json_parser import (
    parse_json
)

def extract_task(email):

    prompt = f"""
TASK: Determine if the email requires the user to take a real action, and extract it as a task.

═══════════════════════════════════════
ABSOLUTE OUTPUT RULES (never violate):
═══════════════════════════════════════
1. Output MUST start with {{ and end with }}
2. No markdown. No code fences. No preamble. No explanation.
3. NEVER invent task titles, descriptions, or due dates not stated in the email.
4. NEVER use relative dates — only return exact YYYY-MM-DD dates.
5. If no real actionable task exists → return the NO-TASK object below. Nothing else.

══════════════════════════════════════════════
OUTPUT SCHEMA — When a real task IS found:
══════════════════════════════════════════════
{{
    "has_task": true,
    "task_type": "<see TASK TYPE RULES>",
    "title": "<short imperative title, e.g. Pay Invoice #1234>",
    "description": "<1-2 sentences: what must be done and why>",
    "due_date": "<YYYY-MM-DD or null>",
    "priority": "<LOW | MEDIUM | HIGH>"
}}

══════════════════════════════════════════════
OUTPUT SCHEMA — When NO real task is found:
══════════════════════════════════════════════
{{
    "has_task": false
}}

════════════════════════
DUE DATE FORMAT RULES:
════════════════════════
due_date MUST always be: YYYY-MM-DD or null

✓ CORRECT:  "2026-06-15"
✓ CORRECT:  null  (if no specific date is stated)
✗ WRONG:    "Soon"
✗ WRONG:    "Tomorrow"
✗ WRONG:    "Next Week"
✗ WRONG:    "2 days from now"
✗ WRONG:    "No specific due date mentioned"
✗ WRONG:    "Limited-time"

RULE: If the date is vague or relative → set due_date to null.
RULE: Only return a date if an explicit calendar date (day + month + year) appears in the email.

═══════════════════
TASK TYPE RULES:
═══════════════════
PAYMENT         → pay a bill, invoice, subscription, or fee
FOLLOW_UP       → reply to someone, check back, send information
APPLICATION     → submit a form, apply for something, register
ASSIGNMENT      → complete a work task, project, or deliverable
MEETING_PREP    → prepare for a scheduled call or meeting
ACTION_REQUIRED → any other time-sensitive user action

════════════════════
PRIORITY RULES:
════════════════════
HIGH   → payment overdue or due within 3 days, security action, legal deadline
MEDIUM → task due within 1-2 weeks, direct request from a person
LOW    → optional follow-up, soft deadline, no explicit urgency stated

══════════════════════════════════════════════
EMAILS THAT MUST ALWAYS RETURN has_task: false
══════════════════════════════════════════════
These email types NEVER generate tasks:
  ✗ Newsletters and digest emails
  ✗ Promotional and marketing emails
  ✗ AI news and product announcements
  ✗ Social media activity (Pinterest, Reddit, LinkedIn)
  ✗ Reports and analytics summaries
  ✗ Informational updates with no user action needed
  ✗ Partnership or product launch announcements
  ✗ Advertisements and discount campaigns
  ✗ Gamification / engagement emails (Duolingo, streaks)

RULE: Only return has_task: true if the USER must DO something specific.
RULE: Reading an email is NOT a task. Being informed is NOT a task.

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
                    "content": "You are a JSON-only actionable task extractor. You output one valid JSON object. Nothing else."
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