# from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import sys
import time
import re
# from argparse import ArgumentParser

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
# SAMPLE_RANGE_NAME = 'Class Data!A2:E'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    if len(sys.argv) < 2:
        url = ''
        while not url:
            url = input('Paste in the spreadsheet URL by right clicking\n')
    else: url = sys.argv[1]
    regex = r'(?<=\/d\/)[^/]*'
    SPREADSHEET_ID = re.search(regex, url).group(0)

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    possible_sheet_names = ['IPP01', 'IPP 1']
    RANGE_NAME = 'IPP 1!A19:H'
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # print(row)
            # break
            # Print columns A and H, which correspond to indices 0 and 7.
            try:
                print('%s \t %s' % (row[0], row[7]))
            except IndexError:
                pass

if __name__ == '__main__':
    print(sys.argv[1:])
    # time.sleep(30)
    main()
