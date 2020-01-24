from .message_abs import MessageAbs
import re


class GeneralMessage(MessageAbs):

    @classmethod
    def bank_name(cls):
        return 'bhdleon'

    @classmethod
    def bank_email(cls):
        return 'alertas@bhdleon.com.do'

    @classmethod
    def get_subjects(cls):
        return [
            'Alerta BHDLeón'
        ]

    @property
    def date(self):
        return self.get_element_by_class('td', 'class', 't_fecha').text

    @property
    def currency(self):
        return self.get_element_by_class('td', 'class', 't_moneda').text

    @property
    def amount(self):
        value = 0
        try:
            value = self.get_element_by_class('td', 'class', 't_monto').text
            value = float(value)
        except ValueError:
            pass
        return value

    @property
    def merchant(self):
        merchant_name = self.get_element_by_class('td', 'class', 't_comercio')
        merchant_name = merchant_name.text if merchant_name else 'None'
        return merchant_name

    @property
    def status(self):
        return self.get_element_by_class('td', 'class', 't_estado').text

    @property
    def type(self):
        return self.get_element_by_class('td', 'class', 't_tipo').text


class PINPesoMessage(MessageAbs):

    def __init__(self):
        self.message_text = ''
        return super().__init__()

    @classmethod
    def bank_name(cls):
        return 'bhdleon'

    @classmethod
    def bank_email(cls):
        return 'alertas@bhdleon.com.do'

    @classmethod
    def get_subjects(cls):
        return [
            'Notificacion de Retiro de PIN Pesos'
        ]

    def feed(self, raw_html: str):
        super().feed(raw_html)
        self.message_text = self.get_elements_by_tag('p')[0].text if self.get_elements_by_tag('p') else ''

    @property
    def date(self):
        date_value = re.findall(r'\d{2}/\d{2}/\d{4}', self.message_text)
        date_value = date_value[0] if date_value else 'None'
        return date_value

    @property
    def currency(self):
        return 'RD'

    @property
    def amount(self):
        value = 0
        try:
            value = re.findall(r'\$\d+,?\d+', self.message_text)
            value = float(value[0][1:].replace(',', ''))
        except ValueError:
            pass
        return value

    @property
    def merchant(self):
        number = re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', self.message_text)
        merchant_name = number[0] if number else 'None'
        merchant_name = f'PIN Pesos - {merchant_name}'
        return merchant_name

    @property
    def status(self):
        return 'Aprobada'

    @property
    def type(self):
        return 'Retiro de Efectivo'

