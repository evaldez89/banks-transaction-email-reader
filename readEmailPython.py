from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


# def main():
#     flow = Flow.from_client_secrets_file(
#         'token.json', 
#         scopes=['profile', 'email'],
#         redirect_uri='urn:ietf:wg:oauth:2.0:oob')

def main():
    #     flow = Flow.from_client_secrets_file(
    #         'token.json', 
    #         scopes=['profile', 'email'],
    #         redirect_uri='urn:ietf:wg:oauth:2.0:oob')
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = Flow.from_client_secrets_file(
        'token.json',
        scopes=SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob')
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v3', http=creds.authorize(Http()))


if __name__ == '__main__':
    main()

print('wei')