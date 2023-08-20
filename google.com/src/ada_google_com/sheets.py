"""
Google Sheet API
"""
from typing import Any, Dict, Iterable, List, Optional, Sequence, cast

import re
import sys
from datetime import datetime, timedelta
from enum import Enum

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource, build
from pydantic import BaseModel

SCOPES = (
    'https://www.googleapis.com/auth/spreadsheets.readonly',
)


class HeadIndex(BaseModel):
    """
    Wrapper for first row in spreadsheet

    Example::

        ------------------------------------------------------------------------
        | Name      | User | Email        | Last time logged In                |
        | gmail.com | A1   | a1@gmail.com | 2022.12.28                         |
        |           |       |             | notify if when: more than 180 days |
        ------------------------------------------------------------------------

    """
    class Fields(Enum):
        """
        Fields variants to be considered as accepted values.
        """
        NAME: Sequence[str] = ('Name',)
        USER: Sequence[str] = ('User', 'Public Name')
        EMAIL: Sequence[str] = ('Email',)
        LAST_TIME_LOGGED_IN: Sequence[str] = ('Last time logged In',)

    name: int
    user: int
    email: int
    last_time_logged_in: int
    sheet_name: str

    @classmethod
    def from_sheet_head(cls, head: Sequence[str], sheet_name: str) -> 'HeadIndex':
        """Factory method to construct object from header"""
        kwarg = {
            k: cls._parse(
                field_name=k,
                head=head,
                accepted_values=getattr(cls.Fields, k.upper()).value,
                sheet_name=sheet_name,
            ) for k in ('name', 'user', 'email', 'last_time_logged_in')
        }

        return cls(sheet_name=sheet_name, **kwarg)

    @staticmethod
    def _parse(field_name: str,
               head: Sequence[str],
               accepted_values: Sequence[str],
               sheet_name: str) -> int:
        """Parse header to extract name, user, email, last_time_logged_in"""
        for name in accepted_values:
            if name in head:
                return head.index(name)

        raise ValueError(f'No {field_name!r} {accepted_values!r} field to be processed in sheet '
                         f'{sheet_name!r}')


class Foot(BaseModel):
    """
    Wrapper for last row in spreadsheet

    Example::

        ------------------------------------------------------------------------
        | Name      | User | Email        | Last time logged In                |
        | gmail.com | A1   | a1@gmail.com | 2022.12.28                         |
        |           |       |             | notify if when: more than 180 days |
        ------------------------------------------------------------------------

    """
    notify_after_n_days: int

    @classmethod
    def from_sheet_foot_and_head_index(cls, foot: Sequence[str], head_index: HeadIndex) -> 'Foot':
        """Factory method to construct object from raw footer and HeadIndex"""
        notify_after_n_days = cls._extract_notify_after_n_days_value(
            foot=foot,
            head_index=head_index
        )

        return cls(notify_after_n_days=notify_after_n_days)

    @staticmethod
    def _extract_notify_after_n_days_value(foot: Sequence[str], head_index: HeadIndex) -> int:
        try:
            notify_after_n_days_raw_value = foot[head_index.last_time_logged_in]
        except IndexError as index_error:
            raise IndexError(
                f'Footer {foot!r} does not contain '
                f'{head_index.Fields.LAST_TIME_LOGGED_IN.value!r} field'
            ) from index_error

        regexp = re.compile(
            r'Notify if when: more than (\d+) days',
            re.IGNORECASE
        )
        match = regexp.search(notify_after_n_days_raw_value)
        if not match:
            print(f'Can not match {regexp.pattern}')
            sys.exit(1)

        return int(match.group(1))


class Source(BaseModel):
    """
    Wrapper for configuration

    Example::

        ------------------------------------------------------------------------
        <Head: see HeadIndex implementation>
        <Raw Content>
        <Foot: See Foot Implementation>
        ------------------------------------------------------------------------

    """
    spreadsheet_id: str
    sheet_name: str
    raw_content: Sequence[Sequence[str]]
    head_index: HeadIndex
    foot: Foot

    @classmethod
    def from_config(cls,
                    spreadsheet_id: str,
                    sheets: Sequence[str],
                    credentials: Credentials) -> Iterable['Source']:
        """
        Factory method to create a Source object, by:

        - fetch sheet info form google api on spreadsheet_id and sheet_name
        - extract header, content and footer
        """
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()  # pylint: disable=no-member
        output = []
        for sheet_name in sheets:
            output.append('INFO Fetching Source(%r, %r)' % (  # pylint: disable=consider-using-f-string
                spreadsheet_id, sheet_name
            ))

            fetch_result = cls._fetch(
                sheet=sheet,
                spreadsheet_id=spreadsheet_id,
                sheet_name=sheet_name
            )

            raw_head, *raw_content, raw_footer = fetch_result.get('values', [])

            head_index = HeadIndex.from_sheet_head(
                sheet_name=sheet_name,
                head=raw_head
            )
            foot = Foot.from_sheet_foot_and_head_index(
                foot=raw_footer,
                head_index=head_index,
            )

            yield Source(
                spreadsheet_id=spreadsheet_id,
                sheet_name=sheet_name,
                raw_content=raw_content,
                head_index=head_index,
                foot=foot
            )

    def _process_content_single_line(self, row: Sequence[str]) -> Optional[str]:
        now = datetime.utcnow()

        last_date_checked_in = row[self.head_index.last_time_logged_in]
        if last_date_checked_in == 'skip':
            return None

        name = row[self.head_index.name]
        user = row[self.head_index.user]
        email = row[self.head_index.email]

        date = datetime.strptime(last_date_checked_in, '%Y.%m.%d')
        if (now - date) > timedelta(days=self.foot.notify_after_n_days):
            return (
                'You have to log into to refresh account, '
                f'you could loose that account .... {repr(name)!r}, {user!r}, {email!r}'
            )

        return None

    @staticmethod
    def _fetch(sheet: Resource, spreadsheet_id: str, sheet_name: str) -> Dict[str, Sequence[str]]:
        """
        Call Google Sheet API for sheet content
        """
        return cast(Dict[str, Sequence[str]], sheet.values().get(
            spreadsheetId=spreadsheet_id,
            range=sheet_name
        ).execute())

    def process_raw_content(self) -> Sequence[str]:
        """
        Process raw content
        """

        output = [f'INFO: will notify after {self.foot.notify_after_n_days} days']

        for row in self.raw_content:
            info = self._process_content_single_line(row)

            if info:
                output.append(info)

        if len(output) == 1:
            output.append(
                'INFO: all %r accounts are up to date '  # pylint: disable=consider-using-f-string
                'and do not need a notification' % len(self.raw_content))

        return output


def check_process_expiration_date(
        credentials: Credentials,
        config: Dict[str, Any]) -> Sequence[str]:
    """
    Based on configuration process all sheets.
    """
    sources = config['spreadsheets']
    output: List[str] = []
    for source_config in sources:
        for source in Source.from_config(
            spreadsheet_id=source_config['spreadsheet_id'],
            sheets=source_config['sheets'],
            credentials=credentials
        ):
            output += source.process_raw_content()

    return output
