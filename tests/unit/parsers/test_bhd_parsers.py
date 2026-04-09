from pathlib import Path

import pytest

from banks_mail_readers.bhd_messages import GeneralMessage, PINPesoMessage

FIXTURES = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


class TestBhdGeneralMessageMetadata:
    def test_bank_name(self):
        assert GeneralMessage.bank_name() == "bhd"

    def test_sender_email(self):
        assert GeneralMessage.sender_email() == "alertas@bhd.com.do"

    def test_supported_subjects(self):
        assert "BHD Notificación de Transacciones" in GeneralMessage.supported_subjects()


class TestBhdGeneralMessageParsing:
    def setup_method(self):
        self.parser = GeneralMessage()
        self.parser.feed(load_fixture("bhd_general.html"))

    def test_date(self):
        assert self.parser.date == "06/04/2026 01:52 pm"

    def test_currency(self):
        assert self.parser.currency == "RD"

    def test_amount(self):
        assert self.parser.amount == 925.0

    def test_merchant(self):
        assert self.parser.merchant == "PedidosYa*Little Caesar"

    def test_status(self):
        assert self.parser.status == "Aprobada"

    def test_type(self):
        assert self.parser.type == "Compra"


class TestBhdGeneralMessageEdgeCases:
    def test_no_table_trans_returns_empty_strings(self):
        parser = GeneralMessage()
        parser.feed("<html><body></body></html>")
        assert parser.date == ""
        assert parser.currency == ""
        assert parser.merchant == ""
        assert parser.status == ""
        assert parser.type == ""

    def test_no_table_trans_returns_zero_amount(self):
        parser = GeneralMessage()
        parser.feed("<html><body></body></html>")
        assert parser.amount == 0

    def test_amount_with_dollar_sign_is_parsed(self):
        parser = GeneralMessage()
        parser.feed(
            '<html><body><table class="table_trans">'
            "<tbody><tr>"
            "<td>date</td><td>RD</td><td>$1,250.50</td>"
            "<td>merchant</td><td>Aprobada</td><td>Compra</td>"
            "</tr></tbody></table></body></html>"
        )
        assert parser.amount == pytest.approx(1250.50)

    def test_no_feed_defaults(self):
        parser = GeneralMessage()
        assert parser.date == ""
        assert parser.amount == 0


class TestBhdPinPesoMessageParsing:
    def setup_method(self):
        self.parser = PINPesoMessage()
        self.parser.feed(load_fixture("bhd_pin_peso.html"))

    def test_inherits_bank_name(self):
        assert PINPesoMessage.bank_name() == "bhd"

    def test_date(self):
        assert self.parser.date == "22/01/2020"

    def test_currency(self):
        assert self.parser.currency == "RD"

    def test_amount(self):
        assert self.parser.amount == pytest.approx(2500.0)

    def test_merchant(self):
        assert self.parser.merchant == "PIN Pesos - 809-555-1234"

    def test_status(self):
        assert self.parser.status == "Aprobada"

    def test_type(self):
        assert self.parser.type == "Retiro de Efectivo"
