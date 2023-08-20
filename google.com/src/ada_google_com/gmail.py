"""
GMail API calls
"""
import base64
from email.message import EmailMessage

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = (
    'https://www.googleapis.com/auth/gmail.send',
)


def check_starred_emails() -> None:
    """
    TODO: add docstring
    """
    raise NotImplementedError()


def check_priority_emails() -> None:
    """
    TODO: add docstring
    """
    raise NotImplementedError()


def send_email(
        credentials: Credentials,
        subject: str,
        to: str,  # pylint: disable=invalid-name
        from_: str,
        content: str) -> None:
    """
    Send Email wrapper
    """
    service = build('gmail', 'v1', credentials=credentials)
    message = EmailMessage()

    message.set_content(content)

    message['To'] = to
    message['From'] = from_
    message['Subject'] = subject

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
        .decode()

    create_message = {
        'raw': encoded_message
    }
    messages = service.users().messages()  # pylint: disable=no-member

    send_message = messages.send(
        userId="me", body=create_message
    ).execute()
    print(F'Message Id: {send_message["id"]}')
