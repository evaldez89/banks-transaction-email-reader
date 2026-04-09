import os
import pickle
import tempfile
from typing import Any

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_credentials_paths() -> tuple[str, str]:
    credential_file = os.getenv("EMAIL_CREDENTIALS_FILE", "credentials.json")
    token_file = os.getenv("EMAIL_TOKEN_FILE", f"{tempfile.gettempdir()}/token.pickle")
    return credential_file, token_file


def load_or_create_credentials(
    credentials: Any = None,
    scopes: list[str] | None = None,
) -> Any:
    scopes = scopes or SCOPES
    credential_file, token_file = get_credentials_paths()

    current_credentials = credentials

    if os.path.exists(token_file):
        with open(token_file, "rb") as token_stream:
            current_credentials = pickle.load(token_stream)

    if not current_credentials or not current_credentials.valid:
        if (
            current_credentials
            and current_credentials.expired
            and current_credentials.refresh_token
        ):
            current_credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credential_file, scopes)
            current_credentials = flow.run_local_server(port=0)

        with open(token_file, "wb") as token_stream:
            pickle.dump(current_credentials, token_stream)

    return current_credentials
