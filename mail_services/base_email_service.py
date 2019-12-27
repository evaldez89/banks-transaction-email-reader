from datetime import date, datetime, timedelta


class EmailService():
    def __init__(self, days_from: int):
        self.name = 'Base Service'
        self.credentials = None
        self.service = None
        self.date_to = date.today()
        self.date_from = self.date_to - timedelta(300)

    def get_query(self, bank_email):
        query = f'before: {self.date_to:%Y/%m/%d}'
        query += f' after: {self.date_from:%Y/%m/%d}'
        query += f' from:{bank_email}'

        return query

    def authenticate(self):
        raise NotImplementedError

    def build_service(self):
        raise NotImplementedError

    def query_mail(self):
        raise NotImplementedError

    def read_mail(self):
        raise NotImplementedError
