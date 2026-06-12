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