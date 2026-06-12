from services.groq_service import client


def answer_question(
    question,
    context
):

    prompt = f"""
You are MailMind AI.

Answer the user's question
using ONLY the provided email data.

If the answer is not present,
say you cannot find it.

Question:

{question}

Email Data:

{context}
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
            temperature=0.2
        )
    )

    return (
        response
        .choices[0]
        .message.content
    )