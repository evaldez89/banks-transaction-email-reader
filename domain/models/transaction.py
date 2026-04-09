from dataclasses import dataclass


@dataclass(frozen=True)
class Transaction:
    date: str
    currency: str
    amount: float
    merchant: str | None
    status: str
    type: str
    bank: str
    source_subject: str
