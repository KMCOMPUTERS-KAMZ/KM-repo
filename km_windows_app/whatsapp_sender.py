from __future__ import annotations

import requests


def send_whatsapp_summary(
    sid: str,
    auth_token: str,
    from_number: str,
    to_number: str,
    message: str,
) -> None:
    """Send WhatsApp using Twilio WhatsApp API."""
    url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"
    payload = {
        "From": f"whatsapp:{from_number}",
        "To": f"whatsapp:{to_number}",
        "Body": message[:1500],
    }
    response = requests.post(url, data=payload, auth=(sid, auth_token), timeout=30)
    response.raise_for_status()
