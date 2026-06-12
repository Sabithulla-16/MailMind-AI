from services.groq_service import client


def generate_digest(rows):

    email_text = []

    for row in rows:

        email_text.append(
            f"""
Category:
{row.get('category')}

Priority:
{row.get('priority')}

Summary:
{row.get('detailed_summary')}
"""
        )

    prompt = f"""
You are an executive assistant.

Create a professional daily inbox summary.

Format exactly like this:

Today's inbox contained X emails.

Highlights:
• ...
• ...
• ...

Finance:
• ...

AI News:
• ...

Account Changes:
• ...

Security:
• ...

Action Required:
Only mention emails where action_required=true.

Rules:

- Only report facts from emails.
- Do NOT suggest optional actions.
- Do NOT recommend things to explore.
- Do NOT invent information.
- Keep under 150 words.
- Use bullet points.
- Focus on the most important updates.

Emails:

{chr(10).join(email_text)}
"""

    response = (
        client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )
    )

    return (
        response
        .choices[0]
        .message.content
    )