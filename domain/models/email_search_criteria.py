from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class EmailSearchCriteria:
    date_from: date
    date_to: date
    sender_email: str | None = None
