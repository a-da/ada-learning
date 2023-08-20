# pylint: disable=missing-module-docstring
from unittest import mock

from ada_google_com import gmail


def test_process_all_sources():
    """
    GIVEN GMail API
    WHEN send email
    THEN send().execute() API will be executed
    """
    with \
            mock.patch.object(gmail, gmail.build.__name__) as build, \
            mock.patch.object(gmail, gmail.EmailMessage.__name__) as email_message:

        email_message.return_value.as_bytes.return_value = b'some bytes'

        gmail.send_email(
            credentials=None,
            subject='some-subject',
            to='to-someone',
            from_='from-someone',
            content='some-content',
        )

        # check GMail send API
        (
            build.return_value
            .users.return_value
            .messages.return_value
            .send.return_value
        ).execute.assert_called_once()

        # check email inputs it match with expected config
        for mock_call in (
                mock.call.set_content('some-content'),
                # pylint: disable=unnecessary-dunder-call
                mock.call.__setitem__('To', 'to-someone'),
                mock.call.__setitem__('From', 'from-someone'),
                mock.call.__setitem__('Subject', 'some-subject'),
                # pylint: enable=unnecessary-dunder-call
        ):
            assert mock_call in email_message.return_value.mock_calls
