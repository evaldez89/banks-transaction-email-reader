import os.path
import pickle
import tempfile
from datetime import date, datetime, timedelta

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from banks_mail_readers.base_reader import BaseReader
from banks_mail_readers.message_abs import MessageAbs

from .base_email_service import EmailService

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailService(EmailService):
    def __init__(self, message_tempalte: MessageAbs, days_from: int):
        super().__init__(message_tempalte, days_from)
        self.name = 'Gmail Service'

    def _credentials_need_refresh(self):
        return self.credentials \
            and self.credentials.expired \
            and self.credentials.refresh_token

    def construct_query(self):
        self.query += f' from:{self.message_template.bank_email()} '

        self.query += f"""subject:("{'" OR "'.join(
            self.message_template.subjects
        )}")"""

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

    def fetch_mail(self) -> list:
        self.construct_query()
        results = self.service.users().messages().list(userId='me',
                                                       q=self.query)
        results = results.execute()

        return results.get('messages', [])

    def read_mail(self):
        for message in self.fetch_mail():
            msg = self.service.users().messages().get(userId='me',
                                                    id=message['id'],
                                                    format='full').execute()

            date_format = "%A, %B %d, %Y %I:%M:%S"
            epoc_ms = int(msg['internalDate']) / 1000.0
            date_time_obj = datetime.fromtimestamp(epoc_ms).strftime(date_format)

            bodies = list()
            if msg['payload']['mimeType'] == 'multipart/related':
                for body in msg['payload']['parts']:
                    if body['mimeType'] == 'text/html':
                        bodies.append(body['body']['data'])
            elif msg['payload']['mimeType'] == 'text/html':
                bodies.append(msg['payload']['body']['data'])

            for message_body in bodies:
                self.message_template.feed(self.decode_message_body(message_body))

                line = f"{self.message_template.date}|{self.message_template.currency}|"
                line += f"{self.message_template.amount}|{self.message_template.merchant}|"
                line += f"{self.message_template.status}|{self.message_template.type}\n"

                with open('./test_files/transactions.csv', 'a+') as the_file:
                    the_file.write(line)
