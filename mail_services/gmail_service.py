import os.path
import pickle
import tempfile
from datetime import date, datetime, timedelta

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from banks_mail_readers.base_reader import BaseReader

from .base_email_service import EmailService

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailService(EmailService):
    def __init__(self, days_from: int):
        super().__init__(days_from)
        self.name = 'Gmail Service'

    def _credentials_need_refresh(self):
        return self.credentials \
            and self.credentials.expired \
            and self.credentials.refresh_token

    def authenticate(self):
        # The file token.pickle stores the user's access and refresh tokens,
        # and is created automatically when the authorization flow completes
        # for the first time.
        token_file = f'{tempfile.gettempdir()}/token.pickle'

        # TODO: donde se debe guardar correctamente?
        # credential_files = f'{tempfile.gettempdir()}/credentials.json'
        print(os.getcwd())
        credential_files = 'credentials.json'

        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                self.credentials = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.credentials or not self.credentials.valid:
            if self._credentials_need_refresh():
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credential_files, SCOPES)
                self.credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_file, 'wb') as token:
                pickle.dump(self.credentials, token)

    def build_service(self):
        self.service = build('gmail', 'v1', credentials=self.credentials)

    def fetch_mail(self, bank: BaseReader) -> list:
        query = self.get_query(bank)
        results = self.service.users().messages().list(userId='me',
                                                       q=query)
        results = results.execute()

        return results.get('messages', [])

    def read_mail(self, bank: BaseReader):
        messages = self.fetch_mail(bank)

        for message in messages:
            msg = self.service.users().messages().get(userId='me',
                                                      id=message['id'],
                                                      format='full').execute()

            date_format = "%A, %B %d, %Y %I:%M:%S"
            epoc_ms = int(msg['internalDate']) / 1000.0
            date_time_obj = datetime.fromtimestamp(epoc_ms)\
                .strftime(date_format)

            bodies = list()
            if msg['payload']['mimeType'] == 'multipart/related':
                for body in msg['payload']['parts']:
                    if body['mimeType'] == 'text/html':
                        bodies.append(body['body']['data'])
            elif msg['payload']['mimeType'] == 'text/html':
                bodies.append(msg['payload']['body']['data'])

            for message_body in bodies:
                bank.feed(self.decode_message_body(message_body), subject)

                line = f"{bank.date}|{bank.currency}|"
                line += f"{bank.amount}|{bank.merchant}|"
                line += f"{bank.status}|{bank.type}\n"

                with open('./test_files/transactions.csv', 'a+') as the_file:
                    the_file.write(line)
