import json

from services.groq_service import (
    ask_groq
)


def generate_reply_draft(
    email,
    intent
):

    prompt = f"""<|im_start|>system
You are a JSON-only email reply generator.

Your job is to generate SAFE email drafts.

You MUST never make decisions on behalf of the user.

Output must be exactly one valid JSON object.
<|im_end|>

<|im_start|>user
TASK:
Write a professional email reply FROM the recipient TO the sender.

STRICT RULES:

1. Output MUST be a single valid JSON object.
2. No markdown.
3. No code fences.
4. No explanation.
5. No text outside JSON.
6. NEVER hallucinate names, dates, commitments, purchases, approvals, attendance, or decisions.
7. NEVER thank the sender for their own email.
8. NEVER sign with a name unless explicitly present in the email.
9. Keep the reply concise.

IMPORTANT SAFETY RULES:

If the email is:

- an invitation
- a meeting request
- a travel request
- an event invitation
- a proposal
- a quotation
- a purchase request
- a registration request
- any email requiring a decision

DO NOT:

- accept
- decline
- commit
- promise
- approve
- confirm attendance
- confirm payment
- confirm purchase

Instead:

- acknowledge receipt
- indicate the message is being reviewed
- state that a response or confirmation will follow

The draft should remain neutral unless the sender's intent is purely informational.

OUTPUT FORMAT:

{{
  "subject": "Re: <original subject>",
  "reply": "<email body>"
}}

USER INTENT:
{intent}

EMAIL SUBJECT:
{email["subject"]}

EMAIL BODY:
{email["body"]}

Return ONLY the JSON object.
<|im_end|>"""

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