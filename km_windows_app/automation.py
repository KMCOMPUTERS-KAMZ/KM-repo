from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler
from .config import AppConfig
from .email_client import fetch_recent_emails
from .summarizer import summarize_emails
from .whatsapp_sender import send_whatsapp_summary
from .social_publisher import post_to_facebook


def run_morning_digest(config: AppConfig) -> None:
    all_messages: list[dict] = []
    for account in config.email_accounts:
        all_messages.extend(fetch_recent_emails(account, limit=30))

    summary = summarize_emails(config.openai_api_key, config.openai_model, all_messages)
    send_whatsapp_summary(
        sid=config.twilio_sid,
        auth_token=config.twilio_auth_token,
        from_number=config.twilio_from_whatsapp,
        to_number=config.owner_whatsapp_number,
        message=f"Good morning. Here is your email brief:\n\n{summary}",
    )


def run_social_broadcast(config: AppConfig, message: str) -> None:
    post_to_facebook(config.facebook_page_token, message)


def start_scheduler(config: AppConfig) -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_morning_digest, "cron", hour=6, minute=30, args=[config], id="morning_digest")
    scheduler.start()
    return scheduler
