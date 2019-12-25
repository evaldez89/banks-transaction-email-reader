# -*- coding: latin_1 -*-
from __future__ import print_function

import base64
import os.path
import pickle
from datetime import date, datetime, timedelta

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from httplib2 import Http, ProxyInfo

from banks_mail_readers.bhdleon_reader import BHDLeonHtmlReader
from banks_mail_readers.vimenca_reader import VimencaHtmlReader

today = date.today()
initialDate = today - timedelta(300)  # fecha inicial, 300 días antes de hoy

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    bhd_email = BHDLeonHtmlReader(100)
    
    results = service.users().messages().list(userId='me',labelIds = ['INBOX'], q=bhd_email.query).execute()
    messages = results.get('messages', [])  # TODO: almacenar todos los id's leidos o fechas

    if not messages:
        print('No messages found.')
    else:
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'],  format='full').execute()
            
            epoc_ms = int(msg['internalDate']) / 1000.0
            date_time_obj = datetime.fromtimestamp(epoc_ms).strftime("%A, %B %d, %Y %I:%M:%S")

            if msg['payload']['mimeType'] == 'multipart/related':
                line = ''
                for single_msg in msg['payload']['parts']:
                    if single_msg['mimeType'] == 'text/html':
                        read_msg = base64.urlsafe_b64decode(single_msg['body']['data'])
                        bhd_email.feed(read_msg)
                        line = f"{bhd_email.date}|{bhd_email.currency}|{bhd_email.amount}|{bhd_email.merchant}|{bhd_email.status}|{bhd_email.type}\n"
                
                        with open('transactions.csv', 'a+') as the_file:
                            the_file.write(line)
                    else:
                        print('no se leyó - : ', single_msg['mimeType'], single_msg['filename'])
            else:
                print('no se leyó: ', msg['payload']['mimeType'])

if __name__ == '__main__':
    main()
