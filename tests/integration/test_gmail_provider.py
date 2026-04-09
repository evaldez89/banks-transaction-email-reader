from base64 import urlsafe_b64encode
from unittest.mock import MagicMock, patch

import pytest

from mail_services.gmail.gmail_email_provider import GmailEmailProvider


def _make_provider(bank_name: str = "bhd", days_from: int = 1) -> GmailEmailProvider:
    return GmailEmailProvider(bank_name=bank_name, email_account="me", days_from=days_from)


class TestGmailAuthentication:
    @patch("mail_services.gmail.gmail_email_provider.load_or_create_credentials")
    def test_authenticate_calls_credentials_loader(self, mock_load):
        mock_load.return_value = MagicMock()
        provider = _make_provider()
        provider.authenticate()
        mock_load.assert_called_once()
        assert provider.credentials is not None

    @patch("mail_services.gmail.gmail_email_provider.load_or_create_credentials")
    def test_authenticate_stores_credentials(self, mock_load):
        fake_creds = MagicMock()
        mock_load.return_value = fake_creds
        provider = _make_provider()
        provider.authenticate()
        assert provider.credentials is fake_creds


class TestGmailBuildService:
    @patch("mail_services.gmail.gmail_email_provider.build")
    def test_build_service_calls_google_api(self, mock_build):
        provider = _make_provider()
        provider.credentials = MagicMock()
        provider.build_service()
        mock_build.assert_called_once_with("gmail", "v1", credentials=provider.credentials)

    @patch("mail_services.gmail.gmail_email_provider.build")
    def test_build_service_sets_service_attribute(self, mock_build):
        mock_build.return_value = MagicMock()
        provider = _make_provider()
        provider.credentials = MagicMock()
        provider.build_service()
        assert provider.service is not None


class TestGmailBuildQuery:
    def test_build_query_raises_for_unknown_bank(self):
        provider = _make_provider(bank_name="unknownbank")
        with pytest.raises(ValueError, match="No parser templates"):
            provider.build_query()

    def test_build_query_returns_string_with_date_range(self):
        provider = _make_provider(bank_name="bhd", days_from=7)
        query = provider.build_query()
        assert "before:" in query
        assert "after:" in query
        assert "from:" in query

    def test_build_query_includes_bank_sender_email(self):
        provider = _make_provider(bank_name="bhd")
        query = provider.build_query()
        assert "alertas@bhd.com.do" in query


class TestGmailFetchEmails:
    def _mock_service(self, messages: list[dict], next_page_token: str | None = None) -> MagicMock:
        response: dict = {"messages": messages}
        if next_page_token:
            response["nextPageToken"] = next_page_token

        mock_service = MagicMock()
        mock_service.users().messages().list().execute.return_value = response
        return mock_service

    def test_fetch_emails_returns_list_of_message_dicts(self):
        provider = _make_provider(bank_name="bhd")
        provider.service = self._mock_service([{"id": "msg1"}, {"id": "msg2"}])
        emails = provider.fetch_emails()
        assert len(emails) == 2
        assert emails[0]["id"] == "msg1"

    def test_fetch_emails_returns_empty_list_when_no_messages(self):
        provider = _make_provider(bank_name="bhd")
        provider.service = self._mock_service([])
        emails = provider.fetch_emails()
        assert emails == []

    def test_fetch_emails_follows_pagination(self):
        provider = _make_provider(bank_name="bhd")

        mock_service = MagicMock()
        first_response = {"messages": [{"id": "msg1"}], "nextPageToken": "token123"}
        second_response = {"messages": [{"id": "msg2"}]}

        mock_service.users().messages().list().execute.side_effect = [
            first_response,
            second_response,
        ]
        provider.service = mock_service
        emails = provider.fetch_emails()
        assert len(emails) == 2


class TestGmailGetTransactions:
    def test_get_transactions_returns_empty_when_no_emails(self):
        provider = _make_provider(bank_name="bhd")
        provider.service = MagicMock()
        provider.service.users().messages().list().execute.return_value = {"messages": []}
        result = provider.get_transactions()
        assert result == []

    def test_get_transactions_skips_unrecognized_subject(self):
        provider = _make_provider(bank_name="bhd")

        list_response = {"messages": [{"id": "abc"}]}
        full_message = {
            "payload": {
                "headers": [{"name": "Subject", "value": "Some unrecognized subject"}],
                "mimeType": "text/html",
                "body": {"data": ""},
            }
        }

        mock_service = MagicMock()
        mock_service.users().messages().list().execute.return_value = list_response
        mock_service.users().messages().get().execute.return_value = full_message
        provider.service = mock_service

        result = provider.get_transactions()
        assert result == []


class TestGmailDecodeMessageBody:
    def test_decode_roundtrip(self):
        original = "<html><body>Test content</body></html>"
        encoded = urlsafe_b64encode(original.encode()).decode()
        result = GmailEmailProvider.decode_message_body(encoded)
        assert result == original

    def test_decode_unicode_content(self):
        original = "<html>Transacción: RD$91.12</html>"
        encoded = urlsafe_b64encode(original.encode("utf-8")).decode()
        result = GmailEmailProvider.decode_message_body(encoded)
        assert result == original
