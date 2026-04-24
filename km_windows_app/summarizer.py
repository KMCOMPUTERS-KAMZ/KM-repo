from __future__ import annotations

from openai import OpenAI


PROMPT = """You are an executive assistant.
Summarize these emails into:
1) Must-act-today items
2) FYI items
3) Potential spam/newsletters to ignore
4) A one-line daily brief
Return concise bullets.
"""


def summarize_emails(api_key: str, model: str, emails: list[dict]) -> str:
    if not emails:
        return "No new important emails were found today."

    client = OpenAI(api_key=api_key)
    content = "\n\n".join(
        f"Account: {m['account']}\nFrom: {m['from']}\nSubject: {m['subject']}\nDate: {m['date']}\nBody: {m['body']}"
        for m in emails
    )
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": content},
        ],
        temperature=0.2,
    )
    return response.output_text.strip()
