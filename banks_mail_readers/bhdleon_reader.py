from .base_reader import BaseReader


class BHDLeonHtmlReader(BaseReader):
    def __init__(self):
        return super().__init__('alertas@bhdleon.com.do')

    @property
    def date(self):
        return self.get_element_by_class('td', 'class', 't_fecha').text

    @property
    def currency(self):
        return self.get_element_by_class('td', 'class', 't_moneda').text

    @property
    def amount(self):
        return self.get_element_by_class('td', 'class', 't_monto').text

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
