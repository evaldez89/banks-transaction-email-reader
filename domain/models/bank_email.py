from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class BankEmail:
    subject: str
    sender: str
    html_bodies: list[str]
    received_at: datetime | None = None
