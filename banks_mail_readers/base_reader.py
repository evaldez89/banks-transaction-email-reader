from bs4 import BeautifulSoup, Tag
from datetime import date, datetime, timedelta
from abc import ABC, abstractproperty


class BaseReader(ABC):
    def __init__(self, email: str):
        self.email = email

    def feed(self, raw_html: str):
        self.html = BeautifulSoup(raw_html, 'html.parser')

    @abstractproperty
    def date(self):
        pass

    @abstractproperty
    def currency(self):
        pass

    @abstractproperty
    def amount(self):
        pass

    @abstractproperty
    def merchant(self):
        pass

    @abstractproperty
    def status(self):
        pass

    @abstractproperty
    def type(self):
        pass

    @abstractproperty
    def subjetcs_to_ignore(self):
        pass

    def get_element_by_class(self, element_tag: str,
                             attr: str, attr_value: str) -> Tag:
        return self.html.find(element_tag, {attr: attr_value})

    def get_elements_by_tag(self, tag: str) -> list:
        return [element for element in self.html.select(tag)]
