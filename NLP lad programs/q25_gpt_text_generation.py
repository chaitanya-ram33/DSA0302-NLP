"""Generate text from a prompt using the OpenAI API."""

import os

from openai import OpenAI


def generate_text(prompt):
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("Set the OPENAI_API_KEY environment variable first.")
    client = OpenAI()
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    prompt = "Write a short paragraph explaining why language is useful."
    print(generate_text(prompt))
