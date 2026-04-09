import re

from .bank_email_parser import BankEmailParser


class GeneralMessage(BankEmailParser):
    def __init__(self):
        super().__init__()
        self._cells: list = []

    @classmethod
    def bank_name(cls):
        return "bhd"

    @classmethod
    def bank_email(cls):
        return "alertas@bhd.com.do"

    @classmethod
    def get_subjects(cls):
        return ["BHD Notificación de Transacciones"]

    def feed(self, raw_html: str):
        super().feed(raw_html)
        table = self.get_element_by_class("table", "class", "table_trans")
        rows = table.select("tbody tr") if table else []
        self._cells = rows[0].find_all("td") if rows else []

    def _cell(self, index: int) -> str:
        if index < len(self._cells):
            return self._cells[index].text.strip()
        return ""

    @property
    def date(self):
        return self._cell(0)

    @property
    def currency(self):
        return self._cell(1)

    @property
    def amount(self):
        try:
            raw = self._cell(2).replace("$", "").replace(",", "").strip()
            return float(raw)
        except ValueError:
            return 0

    @property
    def merchant(self):
        return self._cell(3)

    @property
    def status(self):
        return self._cell(4)

    @property
    def type(self):
        return self._cell(5)


class PINPesoMessage(GeneralMessage):
    def __init__(self):
        self.message_text = ""
        super().__init__()

    @classmethod
    def get_subjects(cls):
        return ["Notificacion de Retiro de PIN Pesos"]

    def feed(self, raw_html: str):
        super().feed(raw_html)
        self.message_text = (
            self.get_elements_by_tag("p")[0].text if self.get_elements_by_tag("p") else ""
        )

    @property
    def date(self):
        date_value = re.findall(r"\d{2}/\d{2}/\d{4}", self.message_text)
        date_value = date_value[0] if date_value else ""
        return date_value

    @property
    def currency(self):
        return "RD"

    @property
    def amount(self) -> float:
        try:
            value = re.findall(r"\$\d+,?\d+", self.message_text)
            return float(value[0][1:].replace(",", "")) if value else 0.0
        except ValueError:
            pass
        return 0.0

    @property
    def merchant(self):
        number = re.findall(
            r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})",
            self.message_text,
        )
        merchant_name = number[0] if number else ""
        merchant_name = f"PIN Pesos - {merchant_name}"
        return merchant_name

    @property
    def status(self):
        return "Aprobada"

    @property
    def type(self):
        return "Retiro de Efectivo"
