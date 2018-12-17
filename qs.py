from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from pprint import pprint

# If modifying these scopes, delete the file token.json.
# SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1zck91TIJeLFpzKcQpKpVQIzH3TI42xUQmRFhWHvT3aM'
SAMPLE_RANGE_NAME = 'IPP 1!H79'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    result = service.spreadsheets().get(
                                        spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        ranges=SAMPLE_RANGE_NAME
                                    ).execute()
    # sheet = service.spreadsheets()
    # result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
    #                             range=SAMPLE_RANGE_NAME).execute()
    # body = {
    #     'values': [['test']]
    # }

    # result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
    #     valueInputOption='USER_ENTERED', body=body).execute()
    # values = result.get('values', [])

    pprint(result)
    return

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))

if __name__ == '__main__':
    main()