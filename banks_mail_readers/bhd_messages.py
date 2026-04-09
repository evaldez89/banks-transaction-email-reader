import re

from .bank_email_parser import BankEmailParser


class GeneralMessage(BankEmailParser):
    @classmethod
    def bank_name(cls):
        return "bhd"

    @classmethod
    def bank_email(cls):
        return "alertas@bhd.com.do"

    @classmethod
    def get_subjects(cls):
        return ["BHD Notificación de Transacciones"]

    @property
    def date(self):
        element = self.get_element_by_class("td", "class", "t_fecha")
        return element.text if element else ""

    @property
    def currency(self):
        element = self.get_element_by_class("td", "class", "t_moneda")
        return element.text if element else ""

    @property
    def amount(self):
        value = 0
        try:
            element = self.get_element_by_class("td", "class", "t_monto")
            value = float(element.text) if element else 0
        except ValueError:
            pass
        return value

    @property
    def merchant(self):
        merchant_name = self.get_element_by_class("td", "class", "t_comercio")
        merchant_name = merchant_name.text if merchant_name else ""
        return merchant_name

    @property
    def status(self):
        element = self.get_element_by_class("td", "class", "t_estado")
        return element.text if element else ""

    @property
    def type(self):
        element = self.get_element_by_class("td", "class", "t_tipo")
        return element.text if element else ""


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
            self.get_elements_by_tag("p")[0].text
            if self.get_elements_by_tag("p")
            else ""
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
