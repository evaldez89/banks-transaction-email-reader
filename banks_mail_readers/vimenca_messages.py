from .message import MessageAbs


class GeneralMessage(MessageAbs):

    @classmethod
    def bank_name(cls):
        return 'vimenca'

    @classmethod
    def bank_email(cls):
        return 'internetbanking@vimenca.com'

    @property
    def subjects(self):
        return [
            'Notificación de Transacción',
            'Aviso Retiro de efectivo'
        ]

    def feed(self, raw_html):
        super().feed(raw_html)
        table = [x for x in self.html.findAll('table')]
        table = table[1] if table else None
        if table is not None:
            self.td_elements = table.findAll('td')

    def get_field_value_by_header(self, header_text: str):
        value = None
        header = self.filter_element_by_text(self.td_elements, header_text)
        try:
            field_value = header.find_next_sibling()
            value = field_value.text
        except Exception:
            pass
        return value

    @property
    def date(self):
        return self.get_field_value_by_header('Fecha y Hora')

    @property
    def currency(self):
        value = self.get_field_value_by_header('Monto')
        value = value[:2] if len(value) > 3 else '$'
        return value

    @property
    def amount(self):
        value = 0
        try:
            value = self.get_field_value_by_header('Monto')
            cleaned_value = ''.join([x for x in value if x.isdigit()])
            value = float(cleaned_value) / 100
        except ValueError:
            pass
        return value

    @property
    def merchant(self):
        merchant_name = self.get_field_value_by_header('Comercio')
        return merchant_name if merchant_name else None

    @property
    def status(self):
        return self.get_field_value_by_header('Estado:')

    @property
    def type(self):
        return self.get_field_value_by_header('Tipo de Transacción').strip()