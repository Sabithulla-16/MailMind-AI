import json

from services.groq_service import (
    ask_groq
)


def generate_reply_draft(
    email,
    intent
):

    prompt = f"""
TASK: Write a professional email reply FROM the recipient TO the sender.

═══════════════════════════════════════
ABSOLUTE OUTPUT RULES (never violate):
═══════════════════════════════════════
1. Output MUST start with {{ and end with }}
2. No markdown. No code fences. No explanation. No text outside the JSON.
3. NEVER hallucinate names, titles, dates, prices, order numbers, or any facts not in the email.
4. NEVER sign with a name unless a name is explicitly stated in the email body.
5. NEVER thank the sender for their email (do not write "Thank you for your email" or similar).
6. Keep the reply concise: 3-5 sentences unless the email clearly requires more.
7. Use \\n for line breaks inside the reply string.

═══════════════════════════════════════════
SAFETY RULE — THE MOST IMPORTANT RULE:
═══════════════════════════════════════════
If the email is ANY of the following:
  → An invitation or event request
  → A meeting or interview request
  → A purchase, order, or payment request
  → A proposal, quotation, or contract
  → A registration or sign-up request
  → A travel or accommodation request
  → Any email where the sender expects a YES or NO

Then the reply MUST:
  ✓ Acknowledge that the message was received
  ✓ State that it is being reviewed
  ✓ Indicate a response will follow
  ✓ Remain completely neutral — no commitment, no refusal

The reply MUST NOT contain:
  ✗ Acceptance or confirmation of any kind
  ✗ Decline or rejection of any kind
  ✗ Any promise, approval, or commitment
  ✗ Confirmation of attendance, payment, or purchase

RULE: When in doubt, acknowledge and defer. Never commit.

═══════════════════════════════════
OUTPUT SCHEMA (return exactly this):
═══════════════════════════════════
{{
  "subject": "Re: {email['subject']}",
  "reply": "<full email body using \\n for line breaks>"
}}

═══════════════
CONTEXT:
═══════════════
User Intent: {intent}
Email Subject: {email["subject"]}
Email Body:
{email["body"]}

Now output the JSON object. Start with {{ and end with }}.
"""

    response = ask_groq(
        prompt
    )

    content = (
        response
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

    return json.loads(
        content
    )