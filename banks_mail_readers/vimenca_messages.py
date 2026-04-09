from .bank_email_parser import BankEmailParser


class GeneralMessage(BankEmailParser):
    @classmethod
    def bank_name(cls):
        return "vimenca"

    @classmethod
    def bank_email(cls):
        return "internetbanking@vimenca.com"

    def __init__(self):
        super().__init__()
        self.td_elements: list = []

    @classmethod
    def get_subjects(cls):
        prefix = "Banco Vimenca:"
        return [
            f"{prefix} Notificación de Transacción",
            f"{prefix} Aviso Retiro de efectivo",
        ]

    def feed(self, raw_html):
        super().feed(raw_html)
        tables = [x for x in self.html.findAll("table")] if self.html else []
        table = tables[1] if len(tables) > 1 else None
        self.td_elements = table.findAll("td") if table is not None else []

    def get_field_value_by_header(self, header_text: str) -> str:
        value = ""
        header = self.filter_element_by_text(self.td_elements, header_text)
        try:
            field_value = header.find_next_sibling() if header else None
            value = field_value.text if field_value else ""
        except Exception:
            pass
        return value

    @property
    def date(self) -> str:
        return self.get_field_value_by_header("Fecha y Hora") or ""

    @property
    def currency(self) -> str:
        value = self.get_field_value_by_header("Monto")
        value = value[:2] if len(value) > 3 else "$"
        return value

    @property
    def amount(self) -> float:
        try:
            value = self.get_field_value_by_header("Monto")
            cleaned_value = "".join([x for x in value if x.isdigit()])
            return float(cleaned_value) / 100
        except ValueError:
            pass
        return 0.0

    @property
    def merchant(self) -> str:
        merchant_name = self.get_field_value_by_header("Comercio")
        return merchant_name if merchant_name else ""

    @property
    def status(self) -> str:
        return self.get_field_value_by_header("Estado:") or ""

    @property
    def type(self) -> str:
        return self.get_field_value_by_header("Tipo de Transacción").strip() or ""


class PaymentReceiptMessage(GeneralMessage, BankEmailParser):
    def __init__(self):
        self.tables = list()
        super().__init__()

    @classmethod
    def get_subjects(cls):
        return [
            "Banco Vimenca: Comprobante de pago",
        ]

    def feed(self, raw_html):
        super().feed(raw_html)
        self.tables = [x for x in self.html.findAll("table")] if self.html else []

    @property
    def date(self):
        return self.tables[1].findAll("td")[-3].text

    @property
    def currency(self):
        value = self.tables[1].findAll("td")[-1].text
        return value[:2]

    @property
    def amount(self):
        value = 0
        try:
            value = self.tables[1].findAll("td")[-1].text
            cleaned_value = "".join([x for x in value[3:] if x.isdigit()])
            value = float(cleaned_value) / 100
        except ValueError:
            pass
        return value

    @property
    def merchant(self) -> str:
        merchant_name = self.tables[2].findAll("td")[7].text
        return merchant_name if merchant_name else ""

    @property
    def status(self) -> str:
        return "Aprobada"

    @property
    def type(self) -> str:
        return self.tables[1].findAll("td")[-4].text


class TransactionNotificationMessage(PaymentReceiptMessage, BankEmailParser):
    @classmethod
    def get_subjects(cls):
        return ["Banco Vimenca: Aviso Notificación Transacción ACH"]

    @property
    def date(self):
        value = self.tables[1].findAll("td")[-2].text
        return value

    @property
    def currency(self):
        value = self.tables[2].findAll("td")[-3].text
        return value[:2]

    @property
    def amount(self):
        value = 0
        try:
            value = self.tables[2].findAll("td")[-3].text
            cleaned_value = "".join([x for x in value[3:] if x.isdigit()])
            value = float(cleaned_value) / 100
        except ValueError:
            pass
        return value

    @property
    def merchant(self) -> str:
        merchant_name = self.tables[2].findAll("td")[-5].text
        return merchant_name if merchant_name else ""

    @property
    def status(self):
        return "Aprobada"

    @property
    def type(self):
        return self.tables[2].findAll("td")[-4].text
