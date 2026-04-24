from __future__ import annotations

import imaplib
import email
from email.header import decode_header
from .config import EmailAccount


def _decode_header(value: str) -> str:
    if not value:
        return ""
    chunks = decode_header(value)
    decoded = []
    for chunk, enc in chunks:
        if isinstance(chunk, bytes):
            decoded.append(chunk.decode(enc or "utf-8", errors="ignore"))
        else:
            decoded.append(chunk)
    return "".join(decoded)


def fetch_recent_emails(account: EmailAccount, limit: int = 20) -> list[dict]:
    """Fetch recent emails via IMAP and return normalized text snippets."""
    mails: list[dict] = []
    with imaplib.IMAP4_SSL(account.imap_server, account.imap_port) as client:
        client.login(account.address, account.password)
        client.select("INBOX")
        _, data = client.search(None, "ALL")
        ids = data[0].split()[-limit:]

        for message_id in ids:
            _, msg_data = client.fetch(message_id, "(RFC822)")
            for part in msg_data:
                if not isinstance(part, tuple):
                    continue
                msg = email.message_from_bytes(part[1])
                body = ""
                if msg.is_multipart():
                    for payload in msg.walk():
                        ctype = payload.get_content_type()
                        disp = str(payload.get("Content-Disposition"))
                        if ctype == "text/plain" and "attachment" not in disp:
                            body = payload.get_payload(decode=True).decode(errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")
                mails.append(
                    {
                        "from": _decode_header(msg.get("From", "")),
                        "subject": _decode_header(msg.get("Subject", "")),
                        "date": msg.get("Date", ""),
                        "body": body.strip()[:2000],
                        "account": account.address,
                    }
                )
    return mails
