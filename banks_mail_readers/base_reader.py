from bs4 import BeautifulSoup, Tag
from datetime import date, datetime, timedelta
from abc import ABC, abstractproperty
from .message_factory import MessageFactory
from .message import MessageAbs
from typing import List


class BaseReader(ABC):
    message_factory = MessageFactory()

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

