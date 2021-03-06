from googleapiclient.discovery import build as googleapiclient_build
from httplib2 import Http
from oauth2client import file, client, tools
from pprint import pprint
import re
import json
from job import marsha, sheet_title


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
# SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

SPREADSHEET_ID = '1H_YWddeM8KaYQf7chWodWb1zUF8tjFz2qxvoKpNYztY'




def main():
    store = file.Storage('job/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('job/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = googleapiclient_build('sheets', 'v4', http=creds.authorize(Http()))
    # spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    # spreadsheet_title = spreadsheet.get('properties').get('title')
    # marsha = get_marsha(spreadsheet_title)
    # sheets = spreadsheet.get('sheets')

    RANGE_NAME = generate_range_name(sheet_title) # sheet
    print(marsha)
    print(sheet_title)
    print(RANGE_NAME)
    print("\n\n\n")
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()

    with open('job/resultSample.json', 'w') as f:
        json.dump(result, f, indent=4)
    return
    """ For Updating Sheets
    body = {
        'values': [['test']]
    }
    result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
        valueInputOption='USER_ENTERED', body=body).execute()
    """


def get_marsha(spreadsheet_title: str) -> str:
    marsha = re.search('(?<=[-_ ])[A-Z]{5}|[A-Z]{5}(?=[-_ ])',
        spreadsheet_title).group()
    return marsha


def generate_range_name(sheet: str) -> str:
    if sheet == 'Landing Page B':
        range_name = sheet + '!N:P'
    else:
        range_name = sheet + '!D:F'
    return range_name


def update_sheet_names():
    store = file.Storage('job/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('job/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = googleapiclient_build('sheets', 'v4', http=creds.authorize(Http()))
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    spreadsheet_title = spreadsheet.get('properties').get('title')
    marsha = get_marsha(spreadsheet_title)
    sheets = spreadsheet.get('sheets')

    sheet_names = []
    for s in sheets:
        title = s.get('properties').get('title')
        sheet_names.append(title)

    with open('job/sheet_names.txt', 'w') as f:
        for s in sheet_names:
            f.write(s + "\n")


def print_sheet_names():
    with open('job/sheet_names.txt', 'r') as f:
        for s in f.readlines():
            print(s)


if __name__ == '__main__':
    main()
