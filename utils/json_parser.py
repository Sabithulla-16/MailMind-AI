import json
import re


def parse_json(content):

    content = (
        content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    match = re.search(
        r"\{.*\}",
        content,
        re.DOTALL
    )

    if not match:
        raise Exception(
            "No JSON found"
        )

    return json.loads(
        match.group()
    )