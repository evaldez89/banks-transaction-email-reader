from .message import MessageAbs


class GeneralMessage(MessageAbs):

    @classmethod
    def bank_name(cls):
        return 'bhdleon'

    @classmethod
    def bank_email(cls):
        return 'alertas@bhdleon.com.do'

    @property
    def subjects(self):
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
