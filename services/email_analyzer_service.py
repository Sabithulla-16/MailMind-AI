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
TASK: Classify the email below into a structured JSON object.

═══════════════════════════════════════
ABSOLUTE OUTPUT RULES (never violate):
═══════════════════════════════════════
1. Output MUST start with {{ and end with }}
2. No markdown. No code fences. No explanation. No preamble.
3. NEVER invent, assume, or infer facts not explicitly stated in the email.
4. NEVER leave any field missing or null — every field is required.
5. If unsure, lower the confidence value. Do NOT guess category or priority.

═══════════════════════════════════
OUTPUT SCHEMA (return exactly this):
═══════════════════════════════════
{{
    "category": "<see CATEGORY RULES>",
    "priority": "<LOW | MEDIUM | HIGH>",
    "short_summary": "<max 15 words>",
    "detailed_summary": "<2-4 sentences>",
    "action_required": <true | false>,
    "confidence": <integer 0-100>
}}

═══════════════════
CATEGORY RULES:
═══════════════════
Map the email to EXACTLY ONE of these categories:

AI_NEWS       → AI model releases, LLM updates, tools like Ollama / OpenAI / Anthropic / Gemini / Groq
FINANCE       → bank statements, transactions, invoices, payment receipts, financial reports
SECURITY      → password changes, suspicious login, 2FA alerts, unauthorized access warnings
ACCOUNT       → account settings, privacy policy changes, connected apps, profile updates
PROMOTION     → marketing emails, discount offers, sales, advertisements, product promotions
NEWSLETTER    → subscriptions, digests, blogs, weekly roundups, informational campaigns
SOCIAL        → social media notifications, friend requests, comments, likes, follows
SHOPPING      → order confirmations, shipping updates, delivery notifications, returns
PERSONAL      → emails from individuals (friends, family, colleagues) with personal context
WORK          → professional tasks, work assignments, HR, company internal communications
IMPORTANT     → legal notices, urgent personal matters, critical deadlines not covered above

RULE: If email fits multiple categories, pick the MOST SPECIFIC one.
RULE: PROMOTION beats NEWSLETTER if a discount or offer is present.
RULE: SECURITY beats ACCOUNT if a threat or alert is present.

═══════════════════
PRIORITY RULES:
═══════════════════
HIGH   → security threats, payment failures, urgent deadlines, legal notices, immediate action needed
MEDIUM → meetings, tasks, work emails, bills due soon, follow-ups
LOW    → newsletters, promotions, social notifications, informational updates

═══════════════════════
SHORT SUMMARY RULES:
═══════════════════════
- Maximum 15 words. Hard limit.
- Summarize the core purpose only.
- No filler words like "This email is about..."

════════════════════════
DETAILED SUMMARY RULES:
════════════════════════
- 2 to 4 sentences only.
- Sentence 1: What happened or what the email contains.
- Sentence 2: Why it matters to the recipient.
- Sentence 3-4 (optional): What the user should know or watch for.
- NEVER include invented details. Only facts from the email.

═══════════════════════
ACTION_REQUIRED RULES:
═══════════════════════
Set to true ONLY IF the user must do one of these:
  ✓ Respond to a security alert or threat
  ✓ Verify identity or account
  ✓ Make or confirm a payment
  ✓ Meet a deadline with consequences
  ✓ Review and reply to a direct request

Set to false FOR:
  ✗ Marketing emails and promotions
  ✗ Newsletters and digests
  ✗ Informational AI news
  ✗ Social notifications
  ✗ Order/shipping confirmations (unless action needed)

══════════════════
CONFIDENCE RULES:
══════════════════
100 = Perfectly clear category with explicit signals
80-99 = Clear category, minor ambiguity
50-79 = Reasonable classification, some uncertainty
0-49 = Low signal email, best-guess classification

═══════════════
EMAIL TO CLASSIFY:
═══════════════
Subject: {subject}
Sender: {sender}
Snippet: {snippet}
Body: {body}

Now output the JSON object. Start with {{ and end with }}.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are a JSON-only email classifier. Your sole output is one valid JSON object. Nothing else."
            },  
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