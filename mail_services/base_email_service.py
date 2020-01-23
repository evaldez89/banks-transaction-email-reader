from abc import ABC, abstractmethod
from base64 import urlsafe_b64decode
from datetime import date, datetime, timedelta
from typing import Any  # TODO: Create base interface for email service to stop using 'Any' as a type

from banks_mail_readers.message_abs import MessageAbs
from banks_mail_readers.message_factory import MessageFactory


class EmailService(ABC):

    date_to = date.today() + timedelta(1)
    messages_factory = MessageFactory()

    def __init__(self, bank_name: str, days_from: int):
        self.name = 'Base Service'
        self.bank_name = bank_name
        self.credentials = None
        self.service: Any = None
        # self.message_template = message_template

        # End date must be tomorrow in order to
        # To Ensure all messages (including today) al fetched
        self.date_from = self.date_to - timedelta(days_from)

        self.query = f'before:{self.date_to:%Y/%m/%d} ' \
                     f'after:{self.date_from:%Y/%m/%d}'

    def construct_query(self):
        pass

    @abstractmethod
    def authenticate(self):
        pass

    @abstractmethod
    def build_service(self):
        pass

    @abstractmethod
    def fetch_mail(self) -> list:
        pass

    @abstractmethod
    def read_mail(self):
        pass

    def decode_message_body(self, encoded_data: str):
        """Decode message body to be able to parse it to HTML.

        Arguments:
            encoded_data {str} -- base64 encode html message

        Returns:
            str -- decoded html message
        """
        return urlsafe_b64decode(encoded_data)

    def get_message_details(self, message_body: str, subject: str):
        message_class = EmailService.messages_factory.get_bank_message_template(self.bank_name, subject)
        if message_class is not None:
            message_template = message_class()
            message_template.feed(self.decode_message_body(message_body))

            try:
                line = f"{message_template.date}|{message_template.currency}|"
                line += f"{message_template.amount}|{message_template.merchant}|"
                line += f"{message_template.status}|{message_template.type}\n"

                return line
            except Exception:
                print(f"Could not read message of bank {self.bank_name} with subject {subject}")

        return False