Scopes
------

1. Get 'last date checked in' columns and check if there are fields that need to be checked again.
   It is necessary to keep some services logged up to date,
    e.g. if gmail account is not used for 2 years it will be deleted which we don't want to happen.

Example of spreadsheet

    ------------------------------------------------------------------------
    | Name      | User | Email        | Last time logged In                |
    | gmail.com | A1   | a1@gmail.com | 2022.12.28                         |
    |           |       |             | notify if when: more than 180 days |
    ------------------------------------------------------------------------

Solution
--------

Get google api and check the dates in the field,
if there are some almost expired dates
send and email with detail what need to be done.

Details
-------

excel
`````

Video
    Follow excellent video tutorial https://www.youtube.com/watch?v=4ssigWmExak.

Read the documentation here
    https://developers.google.com/sheets/api/samples/reading.

https://developers.google.com/sheets/api/quickstart/python

python3 -m venv /opt/python.d/ada-automation/SaaS/google.com

gmail
`````

Api documentation
    https://developers.google.com/gmail/api/quickstart/python
Video
    https://www.youtube.com/watch?v=44ERDGa9Dr4&list=PL3JVwFmb_BnSHlyy3gItOar_Y8w45mbJx

For Developers
--------------

To enable checking spelling please follow instructions from https://stackoverflow.com/a/27162411/1251677.

.. code-block::

    $ brew install svn # required by enchant
    $ brew install enchant
    $ pip install -e '.[dev]'  # it has pyenchant in dependency




