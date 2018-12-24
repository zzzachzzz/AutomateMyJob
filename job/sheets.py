from googleapiclient.discovery import build as googleapiclient_build
from httplib2 import Http
from oauth2client import file, client, tools
from pprint import pprint
from typing import List
import re
import build
import tagging_paths
import pickle

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
# SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

SPREADSHEET_ID = '1H_YWddeM8KaYQf7chWodWb1zUF8tjFz2qxvoKpNYztY'


def main():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = googleapiclient_build('sheets', 'v4', http=creds.authorize(Http()))
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
    print("\n\n\n")
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    """ For Updating Sheets
    body = {
        'values': [['test']]
    }
    result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
        valueInputOption='USER_ENTERED', body=body).execute()
    """
    values = result.get('values')
    # Get rid of lists within the list
    values = [x[0] if len(x) > 0 else '' for x in values]
    pprint(values)
    with open('values.pickle', 'wb') as pickle_file:
        pickle.dump(values, pickle_file)
    print("\n\n\n")

    print("PICKLED")
    # parsed = parse_for_content('Hotel Overview', values)
    # pprint(parsed)
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

def parse_for_content(sheet_title: str, values: List[List[str]]) -> list:
    def complete_build_sequence_piece():
        pass
    marsha = 'TCISI'
    tp = tagging_paths.TaggingPaths(sheet_title, marsha)

    B = build.Build[sheet_title]  # Dictionary with build details
    content_identifiers = build.content_identifiers
    build_sequence = []
    card = sub_card = content = ''
    i = 0
    # while i <= len(values)-1:
    while i <= 7:
        # If blank cell, shouldn't be any after previous filter
        if values[i] == '':
            i += 1
        # If card identifier
        elif values[i] in B:  # 'Intro (A)' in 'Hotel Overview'
            type_ = B.get(values[i]).get('type')
            if type_:
                build_sequence.append(B.get(values[i]))
                pprint(build_sequence)
            else:
                card = values[i]
            i += 1
        # If sub-card identifier
        elif values[i] in B.get(card, {}):
            sub_card = values[i]
            i += 1
        # If content identifier
        # elif values[i] in build_sequence[-1]['ref']
        elif values[i] in content_identifiers:
            if values[i+1] != '':  # Has content in next cell, current is content identifier
                if values[i] in build_sequence[-1].get('ref', []):
                    ref_index = build_sequence[-1]['ref'].index(values[i])
                if 'type' in build_sequence[-1]:
                    build_sequence[-1]['ref'][ref_index] = { values[i]: values[i+1] }
                elif 'type' in build_sequence[-1].get(sub_card, {}):
                    build_sequence[-1][sub_card]['ref'][ref_index] = { values[i]: values[i+1] }
            i += 2
        else:
            i += 1
        

    return build_sequence



if __name__ == '__main__':
    # main()
    with open('values.pickle', 'rb') as pickle_file:
        values = pickle.load(pickle_file)
    pprint(values)
    print("\n\n")
    parsed = parse_for_content('Hotel Overview', values)
    print("\n\n\nFinal:")
    print(parsed)