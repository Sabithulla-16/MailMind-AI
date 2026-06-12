import json
import re

from services.groq_service import client


def analyze_email(email):

    subject = email.get("subject") or ""
    sender = email.get("sender") or ""
    snippet = email.get("snippet") or ""

    body = email.get("body")

    if body is None:
        body = ""

    body = str(body)[:2000]

    prompt = f"""
You are an email classifier.

Analyze the email below.

EMAIL SUBJECT:
{subject}

EMAIL SENDER:
{sender}

EMAIL SNIPPET:
{snippet}

EMAIL BODY:
{body}

Respond with ONLY a JSON object.

{{
    "category": "",
    "priority": "",
    "short_summary": "",
    "detailed_summary": "",
    "action_required": false,
    "confidence": 0
}}

Rules:

category:
AI_NEWS
FINANCE
SOCIAL
PROMOTION
ACCOUNT
SECURITY
NEWSLETTER
PERSONAL
WORK
SHOPPING
IMPORTANT

priority:
LOW
MEDIUM
HIGH

short_summary:
Maximum 15 words.

detailed_summary:
2-4 sentences.
Explain:
- what happened
- why it matters
- what the user should know

action_required:
true only if user should do something.

confidence:
0-100

Classification Rules:

AI releases, LLM updates,
Ollama, OpenAI, Anthropic,
Gemini, Groq updates
= AI_NEWS

Security alerts,
password changes,
suspicious activity
= SECURITY

Account settings,
privacy changes,
connected applications
= ACCOUNT

Marketing emails,
offers,
discounts
= PROMOTION

Return JSON only.

action_required should only be true if:

- account security issue
- payment issue
- verification needed
- user response needed
- important deadline
- required review

Marketing reminders should be false.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={
            "type": "json_object"
        },
        temperature=0
    )

    content = (
        response
        .choices[0]
        .message.content
        .strip()
    )

    try:

        return json.loads(
            content
        )

    except Exception as e:

        print("JSON ERROR")
        print(content)

        return None