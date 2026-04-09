from base64 import urlsafe_b64decode
from datetime import date, timedelta
from typing import Any

from googleapiclient.discovery import build

from domain.models.email_search_criteria import EmailSearchCriteria
from domain.models.transaction import Transaction
from domain.ports.email_provider import EmailProvider
from infrastructure.parsers.registry import bank_parser_registry

from .gmail_auth import SCOPES, load_or_create_credentials

_MULTIPART_MIME_TYPES = {
    "multipart/related",
    "multipart/alternative",
    "multipart/mixed",
}


class GmailEmailProvider(EmailProvider[dict, Transaction]):
    def __init__(
        self,
        bank_name: str,
        email_account: str,
        days_from: int,
    ):
        self.name = "Gmail Email Provider"
        self.bank_name = bank_name
        self.credentials = None
        self.service: Any = None

        self.parser_registry = bank_parser_registry
        self.message_templates = bank_parser_registry.get_bank_messages(self.bank_name)

        date_to = date.today() + timedelta(days=1)
        date_from = date_to - timedelta(days=int(days_from))
        self.search_criteria = EmailSearchCriteria(date_from=date_from, date_to=date_to)

        self.email_account = email_account or "me"

    def authenticate(self) -> None:
        self.credentials = load_or_create_credentials(
            credentials=self.credentials,
            scopes=SCOPES,
        )

    def build_service(self) -> None:
        self.service = build("gmail", "v1", credentials=self.credentials)

    def build_query(self) -> str:
        if not self.message_templates:
            raise ValueError(f"No parser templates found for bank '{self.bank_name}'.")

        bank_email = self.message_templates[0].sender_email()
        self.search_criteria = self.search_criteria.__class__(
            date_from=self.search_criteria.date_from,
            date_to=self.search_criteria.date_to,
            sender_email=bank_email,
        )

        return (
            f"before:{self.search_criteria.date_to:%Y/%m/%d} "
            f"after:{self.search_criteria.date_from:%Y/%m/%d} "
            f"from:{bank_email}"
        )

    def fetch_emails(self) -> list[dict]:
        messages: list[dict] = []

        query = self.build_query()
        response = (
            self.service.users()
            .messages()
            .list(userId=self.email_account, q=query)
            .execute()
        )

        messages.extend(response.get("messages", []))

        while "nextPageToken" in response:
            page_token = response["nextPageToken"]
            response = (
                self.service.users()
                .messages()
                .list(
                    userId=self.email_account,
                    q=query,
                    pageToken=page_token,
                )
                .execute()
            )
            messages.extend(response.get("messages", []))

        return messages

    @staticmethod
    def decode_message_body(encoded_data: str) -> str:
        return urlsafe_b64decode(encoded_data).decode("utf-8")

    def _extract_html_bodies(self, payload: dict) -> list[str]:
        bodies = []
        mime_type = payload.get("mimeType", "")

        if mime_type == "text/html":
            data = payload.get("body", {}).get("data")
            if data:
                bodies.append(data)
        elif mime_type in _MULTIPART_MIME_TYPES:
            for part in payload.get("parts", []):
                bodies.extend(self._extract_html_bodies(part))

        return bodies

    def _read_transactions(self) -> list[Transaction]:
        transactions: list[Transaction] = []

        for message in self.fetch_emails():
            msg: dict = (
                self.service.users()
                .messages()
                .get(userId=self.email_account, id=message["id"], format="full")
                .execute()
            )

            mail_headers = msg.get("payload", {}).get("headers", [])
            subject_values: list[str] = [
                header.get("value", "")
                for header in mail_headers
                if header.get("name", "").lower() == "subject"
            ]
            subject = subject_values[0] if subject_values else ""

            bodies = self._extract_html_bodies(msg.get("payload", {}))
            for message_body in bodies:
                transaction = self._parse_transaction(message_body, subject)
                if transaction is not None:
                    transactions.append(transaction)

        return transactions

    def get_transactions(self) -> list[Transaction]:
        return self._read_transactions()

    def _parse_transaction(self, message_body: str, subject: str) -> Transaction | None:
        message_class = self.parser_registry.get_parser_for_subject(
            self.bank_name, subject
        )
        if message_class is not None:
            message_template = message_class()
            message_template.feed(self.decode_message_body(message_body))

            try:
                return Transaction(
                    date=message_template.date,
                    currency=message_template.currency,
                    amount=message_template.amount,
                    merchant=message_template.merchant,
                    status=message_template.status,
                    type=message_template.type,
                    bank=self.bank_name,
                    source_subject=subject,
                )
            except Exception:
                print(
                    f"Could not read message of bank {self.bank_name} with subject {subject}"
                )

        return None
