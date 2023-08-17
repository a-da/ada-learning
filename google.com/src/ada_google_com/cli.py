"""
Command line interface
"""
import click

from . import common, gmail, sheets

CREDENTIALS = common.get_credentials((
        *gmail.SCOPES,
        *sheets.SCOPES
    ))
CONFIG = common.get_config()


@click.command()
def gmail_check_starred_emails() -> None:
    """TODO: implement"""
    gmail.check_starred_emails()


@click.command()
def gmail_check_priority_emails() -> None:
    """TODO: implement"""
    gmail.check_starred_emails()


@click.command()
def google_sheets_check_process_expiration_date() -> None:
    """
    Read all spreadsheets and sheets,
    and send email notification about founding.
    """
    output = sheets.check_process_expiration_date(CREDENTIALS, CONFIG)
    config = CONFIG['gmail']
    gmail.send_email(
        credentials=CREDENTIALS,
        subject=config['subject'],
        to=config['to'],
        from_=config['from'],
        content='\n'.join(output),
    )


@click.group()
def entry_point() -> None:
    """Entry Point CLI placeholder"""


entry_point.add_command(gmail_check_starred_emails)
entry_point.add_command(gmail_check_priority_emails)
entry_point.add_command(google_sheets_check_process_expiration_date)
