Google provide API used by all of us.
We have our precious data there, let's leverage this with automation.  

## Spreadsheet Challenge

Let's use spreadsheet as tasks, we will refer later as Excel-Reminder.

## Excel-Reminder Features

Get 'last date checked in' columns and check if there are fields that need to be checked again.
It's necessary to keep some services logged up to date,
e.g. if Gmail account isn't used for 2 years it will be deleted which we don't want to happen.

Example of spreadsheet

| Name      |     User      |        Email |                Last time logged In |
|-----------|:-------------:|-------------:|-----------------------------------:| 
| gmail.com |      A1       | a1@gmail.com |                         2022.12.28 |
|           |               |              | notify if when: more than 180 days |


## Solution

Get Google API and check the dates in the field,
if there are some almost expired dates
send and email with detail what need to be done.

## How to run

Before running the script, the Google Workspace has to be configured,
Follow 5 get started steps https://developers.google.com/workspace/guides/get-started:

1. Create a Google Cloud project for your Google Workspace app, extension, or integration.
2. Enable the APIs you want to use in your Google Cloud project.
3. Learn how authentication and authorization works when developing for Google Workspace.
4. Configure OAuth consent to ensure users can understand and approve what access your app has to their data.
5. Create access credentials to authenticate your app's end users or service accounts.


### Provision OS

  ```bash
  $ brew install ansible
  ```

  ```bash
  $ make ansible
  ```

### Set Google Secret File
  
  ```bash
  cp google.com/conf.d/google_com_client_secrets_file.sample.json google.com/conf.d/google_com_client_secrets_file.json
  vim google.com/conf.d/google_com_client_secrets_file.json 
  ```

### Install and Run
  ```bash
  $ source ~/.ada-learningrc # load project specific bash configuration 
  $ make run
  ...
  Please visit this URL to authorize this application:  https://accounts.google.com/o/oauth2...
  
  ```


# References:

## API reference for Google Sheets

Video: Follow excellent video tutorial https://www.youtube.com/watch?v=4ssigWmExak
Text-1: https://developers.google.com/sheets/api/samples/reading
Text-2: https://developers.google.com/sheets/api/quickstart/python


## API reference for Google Mail

Video: https://www.youtube.com/watch?v=44ERDGa9Dr4&list=PL3JVwFmb_BnSHlyy3gItOar_Y8w45mbJx
Text: https://developers.google.com/gmail/api/quickstart/python
