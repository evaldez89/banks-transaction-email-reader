from abc import ABC, abstractmethod
from base64 import urlsafe_b64decode
from datetime import date, datetime, timedelta
from typing import Any  # TODO: Create base interface for email service to stop using 'Any' as a type

from banks_mail_readers.base_reader import BaseReader


class EmailService(ABC):

    date_to = date.today() + timedelta(1)

    def __init__(self, days_from: int):
        self.name = 'Base Service'
        self.credentials = None
        self.service: Any = None
        # End date must be tomorrow in order to
        # To Ensure all messages (including today) al fetched
        self.date_from = self.date_to - timedelta(days_from)

        self.query = f'before:{self.date_to:%Y/%m/%d} ' \
                     f'after:{self.date_from:%Y/%m/%d}'

    def get_query(self, bank: BaseReader):
        self.query += f' from:{bank.email} '

        self.query += f"""subject:("{'" OR "'.join(
            bank.subjetcs_to_include
        )}")"""

        return self.query

    def decode_message_body(self, encoded_data: str):
        """Decode message body to be able to parse it to HTML.

        Arguments:
            encoded_data {str} -- base64 encode html message

        Returns:
            str -- decoded html message
        """
        return urlsafe_b64decode(encoded_data)

    @abstractmethod
    def authenticate(self):
        pass

    @abstractmethod
    def build_service(self):
        pass

    @abstractmethod
    def fetch_mail(self, bank: BaseReader) -> list:
        pass

    @abstractmethod
    def read_mail(self, bank: BaseReader):
        pass
