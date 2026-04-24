from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json

CONFIG_PATH = Path("config.json")


@dataclass
class EmailAccount:
    address: str
    password: str
    imap_server: str
    imap_port: int = 993


@dataclass
class AppConfig:
    owner_whatsapp_number: str = ""
    twilio_from_whatsapp: str = ""
    twilio_sid: str = ""
    twilio_auth_token: str = ""
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    facebook_page_token: str = ""
    instagram_business_account_id: str = ""
    tiktok_access_token: str = ""
    email_accounts: list[EmailAccount] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "owner_whatsapp_number": self.owner_whatsapp_number,
            "twilio_from_whatsapp": self.twilio_from_whatsapp,
            "twilio_sid": self.twilio_sid,
            "twilio_auth_token": self.twilio_auth_token,
            "openai_api_key": self.openai_api_key,
            "openai_model": self.openai_model,
            "facebook_page_token": self.facebook_page_token,
            "instagram_business_account_id": self.instagram_business_account_id,
            "tiktok_access_token": self.tiktok_access_token,
            "email_accounts": [a.__dict__ for a in self.email_accounts],
        }


def load_config() -> AppConfig:
    if not CONFIG_PATH.exists():
        return AppConfig()

    raw = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    accounts = [EmailAccount(**item) for item in raw.get("email_accounts", [])]
    raw["email_accounts"] = accounts
    return AppConfig(**raw)


def save_config(config: AppConfig) -> None:
    CONFIG_PATH.write_text(json.dumps(config.to_dict(), indent=2), encoding="utf-8")
