from bs4 import BeautifulSoup, Tag
from datetime import date, datetime, timedelta

class BaseReader():
    """
    transcation: {
        date        --> 21/12/19 23:40
        currency    --> RD
        amount      --> 100.00
        merchant    --> UBR* PENDING.UBER...
        status      --> Aprovada | Reverzada | Declinada | Rechazada
        type        --> Compra | Crédito | Débito | Consumo
    }
    """
    
    def __init__(self, bank_email: str, days_to_read: int):
        self._date_to = date.today()
        self._date_from = self._date_to - timedelta(days_to_read)
        
        self._query += f'before: {self._date_to:%Y/%m/%d} after: {self._date_from:%Y/%m/%d}'
        self._query += f' from:{bank_email}'

    def feed(self, raw_html: str):
        self.html = BeautifulSoup(raw_html, 'html.parser')

    @property
    def query(self):
        return self._query

    @property
    def date(self):
        raise NotImplementedError

    @property
    def currency(self):
        raise NotImplementedError

    @property
    def amount(self):
        raise NotImplementedError

    @property
    def merchant(self):
        raise NotImplementedError

    @property
    def status(self):
        raise NotImplementedError

    @property
    def type(self):
        raise NotImplementedError

    def get_element_by_class(self, element_tag: str, attr: str, attr_value: str) -> Tag:
        return self.html.find(element_tag, {attr: attr_value})

    def get_elements_by_tag(self, tag: str) -> list:
        return [element for element in self.html.select(tag)]
