# KM Windows Automation App

A Windows-friendly Python desktop app (Tkinter) that helps you:

1. Pull recent email from multiple inboxes.
2. Summarize important messages with an OpenAI model.
3. Send the daily summary to your WhatsApp each morning.
4. Trigger social broadcasting workflows.

> Note: full automation for WhatsApp/Facebook/Instagram/TikTok requires official business APIs, app review, and account approvals.

## Features implemented

- GUI app for entering credentials and running jobs.
- Multiple IMAP email accounts.
- AI-powered summary generation.
- WhatsApp message delivery through Twilio's WhatsApp API.
- Morning scheduler (06:30 local time).
- Social posting scaffold for Facebook, Instagram, and TikTok endpoints.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

## Account format in the UI

In the `Email accounts` box, put one account per line:

```text
email@example.com,password,imap.example.com
```

For your examples, use addresses in valid form:

- `maharajkameel@gmail.com`
- `kameel@kmcomputers.co.za`

## Security recommendations

- Prefer app passwords for email accounts.
- Do not keep production credentials in plain text.
- For production, replace local `config.json` storage with Windows Credential Manager.
