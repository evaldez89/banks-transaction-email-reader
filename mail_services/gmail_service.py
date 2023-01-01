import os.path
import pickle
import tempfile
from datetime import date, datetime, timedelta
from base64 import urlsafe_b64decode
import email

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


            # mime_msg = email.message_from_bytes(urlsafe_b64decode(msg.get("raw")))
            # mime_msg = email.message_from_bytes(urlsafe_b64decode(msg.get("raw")))
            # subject = mime_msg.get('subject')
            # bodies = list()
            # for part in mime_msg.get_payload():
            #     bodies.extend(p.get_payload() for p in part.get_payload() if part.get_default_type() == "text/plain")
            # message_main_type = mime_msg.get_content_maintype()
            # if message_main_type == 'multipart':
            #     for part in mime_msg.get_payload():
            #         part_type = part.get_content_maintype()
            #         part_msg = part.get_payload()
            #         if part_type == 'text':
            #             print(part.get_payload())
            # elif message_main_type == 'text':
            #     print(mime_msg.get_payload())

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
