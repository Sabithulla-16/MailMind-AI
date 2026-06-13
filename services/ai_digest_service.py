from services.groq_service import client
import json

def generate_digest(rows):

    email_blocks = "\n\n".join(
        f"Category: {row.get('category')}\n"
        f"Priority: {row.get('priority')}\n"
        f"Action Required: {row.get('action_required')}\n"
        f"Summary: {row.get('detailed_summary')}"
        for row in rows[:10]
    )

    prompt = f"""
You are an executive assistant.

Create a professional daily inbox summary.

STRICT RULES:

1. Output MUST start with {{ and end with }}
2. No markdown. No code fences. No explanation.
3. NEVER invent facts not present in the email data.
4. NEVER suggest actions or recommendations not in the data.
5. NEVER include an email in action_required unless Action Required is true.
6. Omit any category with zero emails.
7. Each bullet is one concise sentence from the summary.
8. Total bullet text must stay under 150 words.

OUTPUT FORMAT:

{{
    "header": "Today's inbox contained X emails. Y require action.",
    "highlights": [
        "<HIGH priority emails only, max 3 bullets>"
    ],
    "by_category": {{
        "FINANCE": ["<bullet>"],
        "AI_NEWS": ["<bullet>"],
        "SECURITY": ["<bullet>"],
        "ACCOUNT": ["<bullet>"],
        "WORK": ["<bullet>"],
        "NEWSLETTER": ["<bullet>"],
        "PROMOTION": ["<bullet>"],
        "PERSONAL": ["<bullet>"],
        "SOCIAL": ["<bullet>"],
        "SHOPPING": ["<bullet>"],
        "IMPORTANT": ["<bullet>"]
    }},
    "action_required": [
        "<only emails where Action Required is true>"
    ]
}}

SECTION RULES:

highlights:
Only HIGH priority emails.
Max 3 bullets.
Empty array [] if none.

by_category:
Only include categories present in the data.
Max 3 bullets per category.
State what happened. Nothing more.

action_required:
Only emails where Action Required is true.
Empty array [] if none.
No invented deadlines or urgency.

VIOLATION EXAMPLES — never do these:

- "You should review your account settings"
- "Consider exploring the AI tools mentioned"
- "This may require urgent attention"
- Adding an email to action_required when Action Required is false

Return JSON only.

Emails:

{email_blocks}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a JSON-only executive inbox summarizer. Output one valid JSON object. Nothing else."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)