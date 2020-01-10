from abc import ABC, abstractmethod, abstractproperty
from datetime import date, datetime, timedelta

from bs4 import BeautifulSoup, Tag


class MessageAbs(ABC):
    def __init__(self):
        self.html: BeautifulSoup = None

    def feed(self, raw_html: str):
        self.html = BeautifulSoup(raw_html, 'html.parser')

    @classmethod
    @abstractmethod
    def bank_name(cls):
        pass

    @classmethod
    @abstractmethod
    def bank_email(cls):
        pass

    @abstractproperty
    def date(self) -> str:
        pass

    @abstractproperty
    def currency(self) -> str:
        pass

    @abstractproperty
    def amount(self) -> float:
        pass

    @abstractproperty
    def merchant(self) -> str:
        pass

    @abstractproperty
    def status(self) -> str:
        pass

    @abstractproperty
    def subjects(self) -> list:
        pass

    def get_element_by_class(self, element_tag: str,
                             attr: str, attr_value: str) -> Tag:
        return self.html.find(element_tag, {attr: attr_value})

    def get_elements_by_tag(self, tag: str) -> list:
        return [element for element in self.html.select(tag)]

    @staticmethod
    def filter_element_by_text(elements: list, text_critiria: str) -> Tag:
        element = None
        for tag in elements:
            if tag.text.strip() not in ['', '\n'] and \
                    text_critiria in tag.text:
                element = tag
                break

        return element
