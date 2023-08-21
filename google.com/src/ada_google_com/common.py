"""
Internal shared code
"""
from typing import Any, Dict, Sequence, cast

import yaml
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from . import env


def get_credentials(scopes: Sequence[Sequence[str]]) -> Credentials:
    """
    If ``env.TOKEN_JSON`` file exist build credentials offline
    Else fill ``env.TOKEN_JSON`` based on
    Create Credential object based on token.json file based on
    application Flow ``env.CLIENT_SECRETS_FILE``
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    print('[DEBUG] enter function get_credentials')
    if env.TOKEN_JSON.exists():
        print('[DEBUG] env.TOKEN_JSON.exists')
        creds = Credentials.from_authorized_user_file(env.TOKEN_JSON, scopes)
        print('[DEBUG]  Credentials.from_authorized_user_file creds.expired',
              creds.expired)
        print('[DEBUG]  Credentials.from_authorized_user_file creds.refresh_token',
              creds.refresh_token)

    # If there are no (valid) credentials available, let the user log in.

    print('[DEBUG] not creds', not creds)

    if not creds or not creds.valid:
        print('[DEBUG] not creds or not creds.valid')

        # pylint: disable=line-too-long
        # if failed see https://stackoverflow.com/questions/27771324/google-api-getting-credentials-from-refresh-token-with-oauth2client-client
        # pylint: enable=line-too-long
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:

            flow = InstalledAppFlow.from_client_secrets_file(env.CLIENT_SECRETS_FILE, scopes)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        env.TOKEN_JSON.write_bytes(creds.to_json().encode())

    return cast(Credentials, creds)


def get_config() -> Dict[str, Any]:
    """
    Load configuration see sample `google.com/src/conf.d/google_com_config.sample.json`.
    """
    return cast(Dict[str, Any], yaml.safe_load(env.CONFIG.read_bytes()))
