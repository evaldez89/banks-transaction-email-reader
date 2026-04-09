from pathlib import Path

from banks_mail_readers.vimenca_messages import (
    GeneralMessage,
    PaymentReceiptMessage,
    TransactionNotificationMessage,
)

FIXTURES = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


class TestVimencaGeneralMessageMetadata:
    def test_bank_name(self):
        assert GeneralMessage.bank_name() == "vimenca"

    def test_sender_email(self):
        assert GeneralMessage.sender_email() == "internetbanking@vimenca.com"

    def test_supported_subjects_include_transaction(self):
        subjects = GeneralMessage.supported_subjects()
        assert "Banco Vimenca: Notificación de Transacción" in subjects

    def test_supported_subjects_include_withdrawal(self):
        subjects = GeneralMessage.supported_subjects()
        assert "Banco Vimenca: Aviso Retiro de efectivo" in subjects


class TestVimencaGeneralMessageParsing:
    def setup_method(self):
        self.parser = GeneralMessage()
        self.parser.feed(load_fixture("vimenca_general.html"))

    def test_date(self):
        assert self.parser.date == "21/12/19 23:40"

    def test_currency(self):
        assert self.parser.currency == "RD"

    def test_amount(self):
        assert self.parser.amount == 91.12

    def test_merchant(self):
        assert self.parser.merchant == "UBR* PENDING.UBER.COM"

    def test_status(self):
        assert self.parser.status == "Aprobada"

    def test_type(self):
        assert self.parser.type == "Compra"


class TestVimencaGeneralMessageEdgeCases:
    def test_missing_second_table_returns_empty_fields(self):
        parser = GeneralMessage()
        parser.feed("<html><body><table></table></body></html>")
        assert parser.date == ""
        assert parser.currency == "$"
        assert parser.amount == 0.0
        assert parser.merchant == ""
        assert parser.status == ""
        assert parser.type == ""

    def test_no_feed_returns_empty(self):
        parser = GeneralMessage()
        assert parser.date == ""
        assert parser.amount == 0.0


class TestVimencaPaymentReceiptMetadata:
    def test_bank_name(self):
        assert PaymentReceiptMessage.bank_name() == "vimenca"

    def test_subject(self):
        assert "Banco Vimenca: Comprobante de pago" in PaymentReceiptMessage.supported_subjects()


class TestVimencaPaymentReceiptParsing:
    def setup_method(self):
        self.parser = PaymentReceiptMessage()
        self.parser.feed(load_fixture("vimenca_payment_receipt.html"))

    def test_date(self):
        assert self.parser.date == "21/12/19 23:40"

    def test_currency(self):
        assert self.parser.currency == "RD"

    def test_amount(self):
        assert self.parser.amount == 91.12

    def test_merchant(self):
        assert self.parser.merchant == "UBR* PENDING.UBER.COM"

    def test_status_is_always_approved(self):
        assert self.parser.status == "Aprobada"

    def test_type(self):
        assert self.parser.type == "Compra"


class TestVimencaTransactionNotificationMetadata:
    def test_subject(self):
        subjects = TransactionNotificationMessage.supported_subjects()
        assert "Banco Vimenca: Aviso Notificación Transacción ACH" in subjects


class TestVimencaTransactionNotificationParsing:
    def setup_method(self):
        self.parser = TransactionNotificationMessage()
        self.parser.feed(load_fixture("vimenca_transaction_notification.html"))

    def test_date(self):
        assert self.parser.date == "21/12/19 23:40"

    def test_currency(self):
        assert self.parser.currency == "RD"

    def test_amount(self):
        assert self.parser.amount == 91.12

    def test_merchant(self):
        assert self.parser.merchant == "UBR* PENDING.UBER.COM"

    def test_type(self):
        assert self.parser.type == "ACH"

    def test_status_is_always_approved(self):
        assert self.parser.status == "Aprobada"
