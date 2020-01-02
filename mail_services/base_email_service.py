from datetime import date, datetime, timedelta
from base64 import urlsafe_b64decode
from banks_mail_readers.base_reader import BaseReader


class EmailService():

    query = ''
    date_to = date.today() + timedelta(1)

    def __init__(self, days_from: int):
        self.name = 'Base Service'
        self.credentials = None
        self.service = None
        # End date must be tomorrow in order to
        # To Ensure all messages (including today) al fetched
        self.date_from = self.date_to - timedelta(days_from)

        self.query = f'before: {self.date_to:%Y/%m/%d}'
        f' after: {self.date_from:%Y/%m/%d}'

    @classmethod
    def get_query(cls, bank: BaseReader):
        cls.query += f' from:{bank.email} '

        for sbj in bank.subjetcs_to_ignore:
            cls.query += f'-"{sbj}" '

        return cls.query

    def get_message_body(self, encoded_data: str) -> str:
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
