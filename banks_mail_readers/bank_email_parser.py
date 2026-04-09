from abc import ABC, abstractmethod

from bs4 import BeautifulSoup, Tag


class BankEmailParser(ABC):
    def __init__(self):
        self.html: BeautifulSoup | None = None

    def feed(self, raw_html: str):
        self.html = BeautifulSoup(raw_html, "html.parser")

    @classmethod
    @abstractmethod
    def bank_name(cls) -> str: ...

    @classmethod
    def bank_code(cls) -> str:
        return cls.bank_name()

    @classmethod
    @abstractmethod
    def bank_email(cls) -> str: ...

    @classmethod
    def sender_email(cls) -> str:
        return cls.bank_email()

    @classmethod
    @abstractmethod
    def get_subjects(cls) -> list[str]: ...

    @classmethod
    def supported_subjects(cls) -> list[str]:
        return cls.get_subjects()

    @property
    @abstractmethod
    def date(self) -> str: ...

    @property
    @abstractmethod
    def currency(self) -> str: ...

    @property
    @abstractmethod
    def amount(self) -> float: ...

    @property
    @abstractmethod
    def merchant(self) -> str: ...

    @property
    @abstractmethod
    def status(self) -> str: ...

    @property
    @abstractmethod
    def type(self) -> str: ...

    def get_element_by_class(
        self, element_tag: str, attr: str, attr_value: str
    ) -> Tag | None:
        return self.html.find(element_tag, {attr: attr_value}) if self.html else None

    def get_elements_by_tag(self, tag: str) -> list[Tag]:
        return [element for element in self.html.select(tag)] if self.html else []

    @staticmethod
    def filter_element_by_text(elements: list[Tag], text_critiria: str) -> Tag | None:
        element = None
        for tag in elements:
            if tag.text.strip() not in ["", "\n"] and text_critiria in tag.text:
                element = tag
                break

        return element
