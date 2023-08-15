# pylint: disable=missing-module-docstring
import pytest
from click.testing import CliRunner


@pytest.mark.integration
def test_google_sheets_check_process_expiration_date():
    """
    ada_google_com google-sheets-check-process-expiration-date
    """
    from ada_google_com import cli  # pylint: disable=import-outside-toplevel

    runner = CliRunner()
    result = runner.invoke(cli.entry_point, ['google-sheets-check-process-expiration-date'])
    assert result.exit_code == 0
    assert 'Message Id' in result.output
