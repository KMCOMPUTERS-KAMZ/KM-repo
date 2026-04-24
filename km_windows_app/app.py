from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox

from .config import AppConfig, EmailAccount, load_config, save_config
from .automation import run_morning_digest, run_social_broadcast, start_scheduler


class KMApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("KM Windows Automation")
        self.geometry("860x620")
        self.config_data: AppConfig = load_config()
        self.scheduler = None

        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self, padding=16)
        frame.pack(fill="both", expand=True)

        self.owner_whatsapp = self._add_field(frame, "Owner WhatsApp (+countrycode):", self.config_data.owner_whatsapp_number)
        self.twilio_from = self._add_field(frame, "Twilio WhatsApp number:", self.config_data.twilio_from_whatsapp)
        self.twilio_sid = self._add_field(frame, "Twilio SID:", self.config_data.twilio_sid)
        self.twilio_token = self._add_field(frame, "Twilio Auth Token:", self.config_data.twilio_auth_token, show="*")
        self.openai_key = self._add_field(frame, "OpenAI API Key:", self.config_data.openai_api_key, show="*")

        ttk.Label(frame, text="Email accounts (address,password,imap_server)").pack(anchor="w", pady=(8, 0))
        self.email_box = tk.Text(frame, height=8)
        self.email_box.pack(fill="x")
        for account in self.config_data.email_accounts:
            self.email_box.insert("end", f"{account.address},{account.password},{account.imap_server}\n")

        ttk.Label(frame, text="Social post message:").pack(anchor="w", pady=(8, 0))
        self.post_message = tk.Text(frame, height=6)
        self.post_message.pack(fill="x")

        row = ttk.Frame(frame)
        row.pack(fill="x", pady=12)
        ttk.Button(row, text="Save Config", command=self.save).pack(side="left")
        ttk.Button(row, text="Run Morning Digest Now", command=self.run_digest).pack(side="left", padx=8)
        ttk.Button(row, text="Post to Social Now", command=self.post_now).pack(side="left")
        ttk.Button(row, text="Start Daily Scheduler", command=self.start_daily).pack(side="left", padx=8)

        self.status = ttk.Label(frame, text="Ready")
        self.status.pack(anchor="w")

    def _add_field(self, parent: ttk.Frame, label: str, value: str, show: str | None = None) -> ttk.Entry:
        ttk.Label(parent, text=label).pack(anchor="w")
        entry = ttk.Entry(parent, show=show)
        entry.insert(0, value)
        entry.pack(fill="x")
        return entry

    def save(self) -> None:
        self.config_data = self._read_form()
        save_config(self.config_data)
        self.status.config(text="Configuration saved.")

    def run_digest(self) -> None:
        try:
            self.save()
            run_morning_digest(self.config_data)
            self.status.config(text="Morning digest sent via WhatsApp.")
        except Exception as exc:
            messagebox.showerror("Digest failed", str(exc))

    def post_now(self) -> None:
        try:
            self.save()
            message = self.post_message.get("1.0", "end").strip()
            run_social_broadcast(self.config_data, message)
            self.status.config(text="Social post published.")
        except Exception as exc:
            messagebox.showerror("Post failed", str(exc))

    def start_daily(self) -> None:
        self.save()
        if self.scheduler:
            self.scheduler.shutdown(wait=False)
        self.scheduler = start_scheduler(self.config_data)
        self.status.config(text="Daily scheduler active (06:30 local time).")

    def _read_form(self) -> AppConfig:
        rows = [line.strip() for line in self.email_box.get("1.0", "end").splitlines() if line.strip()]
        accounts: list[EmailAccount] = []
        for row in rows:
            parts = [p.strip() for p in row.split(",")]
            if len(parts) != 3:
                raise ValueError(f"Invalid email account row: {row}")
            accounts.append(EmailAccount(address=parts[0], password=parts[1], imap_server=parts[2]))

        return AppConfig(
            owner_whatsapp_number=self.owner_whatsapp.get().strip(),
            twilio_from_whatsapp=self.twilio_from.get().strip(),
            twilio_sid=self.twilio_sid.get().strip(),
            twilio_auth_token=self.twilio_token.get().strip(),
            openai_api_key=self.openai_key.get().strip(),
            email_accounts=accounts,
        )


def main() -> None:
    app = KMApp()
    app.mainloop()


if __name__ == "__main__":
    main()
