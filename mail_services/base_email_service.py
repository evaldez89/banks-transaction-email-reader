from datetime import date, datetime, timedelta
from base64 import urlsafe_b64decode
from banks_mail_readers.base_reader import BaseReader
from typing import Any  # TODO: Create base interface for email service to stop using 'Any' as a type


class EmailService():

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

    def authenticate(self):
        raise NotImplementedError

    def build_service(self):
        raise NotImplementedError

    def query_mail(self):
        raise NotImplementedError

    def read_mail(self):
        raise NotImplementedError
