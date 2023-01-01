import os.path
import pickle
import tempfile

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from banks_mail_readers.message_abs import MessageAbs

from .base_email_service import EmailService

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailService(EmailService):
    def __init__(self, bank_name: str, days_from: int):
        super().__init__(bank_name, days_from)
        self.name = 'Gmail Service'

    def _credentials_need_refresh(self):
        return self.credentials \
            and self.credentials.expired \
            and self.credentials.refresh_token

    def construct_query(self):
        bank_email = self.message_templates[0].bank_email()
        self.query += f' from:{bank_email} '

    def authenticate(self):
        # The file token.pickle stores the user's access and refresh tokens,
        # and is created automatically when the authorization flow completes
        # for the first time.
        token_file = f'{tempfile.gettempdir()}/token.pickle'

        # TODO: donde se debe guardar correctamente?
        # credential_files = f'{tempfile.gettempdir()}/credentials.json'
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
        messages:list = list()

        self.construct_query()
        results = self.service.users().messages().list(userId='me',
                                                       q=self.query)
        response = results.execute()

        messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = self.service.users().messages().list(userId='me',
                                                            q=self.query,
                                                            pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages

    def read_mail(self):
        for message in self.fetch_mail():
            msg = self.service.users().messages().get(userId='me',
                                                      id=message['id'],
                                                      format='full').execute()

            mail_headers = msg.get('payload').get('headers')
            subject = [
                x.get('value') for x in mail_headers
                if x.get('name').lower() == 'subject'
            ]

            subject = subject[0] if len(subject) >= 1 else False

            bodies = list()
            if msg['payload']['mimeType'] == 'multipart/related':
                for body in msg['payload']['parts']:
                    if body['mimeType'] == 'text/html':
                        bodies.append(body['body']['data'])
            elif msg['payload']['mimeType'] == 'text/html':
                bodies.append(msg['payload']['body']['data'])

            for message_body in bodies:

                detail_line = self.get_message_details(message_body, subject)
                if detail_line:
                    with open('./test_files/transactions.csv', 'a+') as the_file:
                        the_file.write(f'{detail_line}')
