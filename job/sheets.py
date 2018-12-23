from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from pprint import pprint
from typing import List
import re
# from . import tagging_paths

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
# SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1H_YWddeM8KaYQf7chWodWb1zUF8tjFz2qxvoKpNYztY'
# RANGE_NAME = 'Hotel Overview!D1:D100'

def main():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    spreadsheet_title = spreadsheet.get('properties').get('title')
    marsha = get_marsha(spreadsheet_title)
    sheets = spreadsheet.get('sheets')
    sheet_names = get_sheet_names(sheets)

    RANGE_NAME = generate_range_name('Hotel Overview') # sheet
    print(spreadsheet_title)
    print(marsha)
    print(sheet_names)
    print(RANGE_NAME)
    # result = service.spreadsheets().values().get(
    #     spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()

    # body = {
    #     'values': [['test']]
    # }
    # result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
    #     valueInputOption='USER_ENTERED', body=body).execute()

    # values = result.get('values')
    # pprint(values)
    # parsed = parse_for_content()
    
    return


def get_marsha(spreadsheet_title: str) -> str:
    marsha = re.search('(?<=[-_ ])[A-Z]{5}|[A-Z]{5}(?=[-_ ])',
        spreadsheet_title).group()
    return marsha


def generate_range_name(sheet: str) -> str:
    if sheet == 'Landing Page B':
        range_name = sheet + '!N:N'
    else:
        range_name = sheet + '!D:D'
    return range_name


def get_sheet_names(sheets: list) -> list:
    sheet_names = []
    for s in sheets:
        title = s.get('properties').get('title')
        sheet_names.append(title)
    return sheet_names

def parse_for_content(sheet_title: str, values: List[List[str]]):
    tp = tagging_paths.TaggingPaths(sheet_title, marsha)
    # :)))))


if __name__ == '__main__':
    main()