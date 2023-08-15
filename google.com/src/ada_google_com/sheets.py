"""
Google Sheet API
"""
from typing import Any, Dict, List, Sequence

import re
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = (
    'https://www.googleapis.com/auth/spreadsheets.readonly',
)


@dataclass
class Source:
    """
    Wrapper for configuration
    """
    spreadsheet_id: str
    sheets: Sequence[str]


def process_head_content_and_footer(  # pylint: disable=too-many-locals
        head: Sequence[str],
        content: Sequence[Sequence[str]],
        footer: Sequence[str],
        sheet_name: str,
        output: List[str],
    ) -> None:
    """
    Process data available in head, content, and footer to send notification if needed
    """
    last_date_checked_in_literal = 'Last time logged In'
    try:
        last_date_checked_in_index = head.index(last_date_checked_in_literal)
    except ValueError as value_error:
        raise ValueError(
            f'No {last_date_checked_in_literal!r} field to be processed in sheet '
            f'{sheet_name!r}'
        ) from value_error

    name_literal = 'Name'
    try:
        name_index = head.index('Name')
    except ValueError as value_error:
        raise ValueError(f'No {name_literal!r} field to be processed in sheet '
                         f'{sheet_name!r}') from value_error

    user_index = head.index('User') if 'User' in head else head.index('Public Name')
    email_index = head.index('Email')

    # notify if when: more than 180 days
    try:
        notify_after_n_days_raw_value = footer[last_date_checked_in_index]
    except IndexError as index_error:
        raise IndexError(
            f'Footer {footer!r} does not contain {last_date_checked_in_index!r}'
        ) from index_error

    regexp = re.compile(
        r'Notify if when: more than (\d+) days',
        re.IGNORECASE
    )
    match = regexp.search(notify_after_n_days_raw_value)
    if not match:
        print(f'Can not mathc {regexp.pattern}')
        sys.exit(1)

    notify_after_n_days = int(match.group(1))

    output.append('INFO: will notify after %r days' % notify_after_n_days)  # pylint: disable=consider-using-f-string

    now = datetime.utcnow()

    assert content
    need_notification = False
    for row in content:
        last_date_checked_in = row[last_date_checked_in_index]
        if last_date_checked_in == 'skip':
            continue

        name = row[name_index]
        user = row[user_index]
        email = row[email_index]

        date = datetime.strptime(last_date_checked_in, '%Y.%m.%d')
        if (now - date) > timedelta(days=notify_after_n_days):
            need_notification = True
            output.append((
                'you have to log into to refresh account, '
                f'you could loose that account .... {repr(name)!r}, {user!r}, {email!r}')
            )

    if not need_notification:
        output.append(
            'INFO: all %r accounts are up to date '  # pylint: disable=consider-using-f-string
            'and do not need a notification' % len(content))


def process_source(credentials: Credentials, source: Source, output: List[str]) -> None:
    """
    Process a concrete spreadsheet sheet
    """

    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()  # pylint: disable=no-member
    for sheet_name in source.sheets:
        output.append('INFO Fetching Source(%r, %r)' % (  # pylint: disable=consider-using-f-string
            source.spreadsheet_id, sheet_name
        ))
        result = sheet.values().get(
            spreadsheetId=source.spreadsheet_id,
            range=sheet_name
        ).execute()

        head, *content, footer = result.get('values', [])
        process_head_content_and_footer(
            head=head,
            content=content,
            footer=footer,
            sheet_name=sheet_name,
            output=output
        )


def check_process_expiration_date(
        credentials: Credentials,
        config: Dict[str, Any]) -> Sequence[str]:
    """
    Based on configuration process all sheets.
    """
    sources = config['spreadsheets']
    output: List[str] = []
    for source in sources:
        process_source(
            credentials=credentials,
            source=Source(
                spreadsheet_id=source['spreadsheet_id'],
                sheets=source['sheets']
            ),
            output=output
        )
    return output
