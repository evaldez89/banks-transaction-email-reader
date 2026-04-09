from abc import ABC, abstractmethod

from domain.models.transaction import Transaction


class BankEmailParser(ABC):
    def __init__(self) -> None:
        self._raw_html = ""

    @classmethod
    @abstractmethod
    def bank_code(cls) -> str:
        """Return canonical bank code (e.g. 'bhd', 'vimenca')."""

    @classmethod
    @abstractmethod
    def sender_email(cls) -> str:
        """Return sender email used to filter source messages."""

    @classmethod
    @abstractmethod
    def supported_subjects(cls) -> list[str]:
        """Return supported email subjects for this parser."""

    def feed(self, raw_html: str) -> None:
        self._raw_html = raw_html

    @abstractmethod
    def parse_transaction(self) -> Transaction:
        """Parse loaded HTML and return a domain transaction."""
