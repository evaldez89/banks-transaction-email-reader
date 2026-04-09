import os
import re
from dataclasses import dataclass

from banks_mail_readers.bank_email_parser import BankEmailParser


@dataclass(frozen=True)
class ParserRegistration:
    bank_code: str
    parser: type[BankEmailParser]


class BankParserRegistry:
    """Explicit parser registry decoupled from subclass auto-discovery."""

    def __init__(self, subject_match_strategy: str | None = None):
        self.subject_match_strategy = (
            (subject_match_strategy or os.getenv("SUBJECT_MATCH_STRATEGY", "exact"))
            .strip()
            .lower()
        )
        self._registrations: list[ParserRegistration] = []

    def register(self, bank_code: str, parser: type[BankEmailParser]) -> None:
        self._registrations.append(
            ParserRegistration(bank_code=bank_code, parser=parser)
        )

    def get_bank_messages(self, bank_name: str) -> list[type[BankEmailParser]]:
        normalized = bank_name.strip().lower()
        return [
            registration.parser
            for registration in self._registrations
            if registration.bank_code == normalized
        ]

    def get_parser_for_subject(
        self, bank_name: str, subject: str
    ) -> type[BankEmailParser] | None:
        for parser in self.get_bank_messages(bank_name):
            if self._matches_subject(
                subject=subject, patterns=parser.supported_subjects()
            ):
                return parser
        return None

    def get_subscribed_banks(self) -> list[dict[str, str]]:
        subscribed = []
        for registration in self._registrations:
            subscribed.append(
                {
                    "main_class": registration.parser.__name__,
                    "module": registration.parser.__module__,
                }
            )
        return subscribed

    def get_available_bank_codes(self) -> list[str]:
        banks = {registration.bank_code for registration in self._registrations}
        return sorted(banks)

    def _matches_subject(self, subject: str, patterns: list[str]) -> bool:
        strategy = self.subject_match_strategy

        if strategy == "regex":
            return any(re.search(pattern, subject) for pattern in patterns)

        return subject in patterns


# Module-level singleton — import and use this instead of instantiating directly.
bank_parser_registry = BankParserRegistry()
