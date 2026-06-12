from services.groq_service import client


def answer_question(
    question,
    context
):

    prompt = f"""
TASK: Answer the user's question using ONLY the email data provided below.

═══════════════════════════════════════
ABSOLUTE ANSWER RULES (never violate):
═══════════════════════════════════════
1. Use ONLY facts that appear in the email data below. Nothing else.
2. If the answer is not present in the email data → respond EXACTLY:
   "I cannot find that information in the provided email data."
3. NEVER guess, infer, or fill in missing details.
4. NEVER reference external knowledge, prior context, or assumptions.
5. Keep the answer concise and direct.
6. If the question is ambiguous, answer the most reasonable interpretation using only the data.

═══════════════════════════════════════
VIOLATION EXAMPLES — never do these:
═══════════════════════════════════════
✗ "The meeting is probably at 10am" — do not speculate
✗ "This is likely from your bank" — do not infer sender identity
✗ "You should reply within 24 hours" — do not add advice not in the data
✗ "Based on typical email patterns..." — do not use general knowledge

═════════════
USER QUESTION:
═════════════
{question}

═══════════
EMAIL DATA:
═══════════
{context}

Now answer the question using only the email data above.
"""

    response = (
        client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are MailMind AI — a grounded, factual email assistant. You answer questions using ONLY the provided email data. You NEVER invent, assume, or infer information that is not explicitly present."
                },
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