from groq import Groq
from utils.config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)


def ask_groq(
    prompt
):

    response = (
        client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a JSON-only safe email draft generator. Your ONLY job is to produce one valid JSON object containing a neutral, professional reply draft. You NEVER make decisions on behalf of the user."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
    )

    return (
        response
        .choices[0]
        .message
        .content
    )


def test_groq():

    return ask_groq(
        "Reply with OK"
    )