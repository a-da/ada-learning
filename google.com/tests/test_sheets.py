# pylint: disable=missing-module-docstring,protected-access
from unittest import mock

from ada_google_com import sheets


def test_check_process_expiration_date():
    """
    GIVEN a Google spreadsheet with an expired field
    WHEN check for expiration date
    THEN get a information about the expiration field
    """
    with mock.patch.object(sheets.Source, sheets.Source._fetch.__name__, return_value={
        'values': [
            ['Name',   'Email',   'User',   'Last time logged In'],
            ['Name-1', 'Email-1', 'User-1', '2000.12.29'],
            ['',       '',        '',        'notify if when: more than 180 days'],
        ]

    }):
        out = sheets.check_process_expiration_date(
            credentials=mock.Mock(),
            config={
                'spreadsheets': [
                    {
                        'spreadsheet_id': 'spreadsheet_id_1',
                        'sheets': ['sheet_1']
                    }
                ]
            }
        )

        assert out == [
            'INFO: will notify after 180 days',
            'You have to log into to refresh account, you could lose that account .... '
            "'Name-1', 'User-1', 'Email-1'",
        ]
