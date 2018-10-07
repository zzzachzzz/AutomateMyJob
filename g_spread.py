import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
from pprint import pprint

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)

url = 'https://docs.google.com/spreadsheets/d/1dNi4S7Y37CUfTb1qevxiJGH5cTbntFmygNriv4oLW40/edit#gid=634087401'
regex = r'(?<=\/d\/)[^/]*'
key = re.search(regex, url).group(0)
wks = gc.open_by_key(key).sheet1

pprint(wks.get_all_values()) # Returns a list of lists

# wks.acell(label)
# wks.cell(row, col)
# wks.col_values(col)
# wks.row_values(row)
# wks.find(query) # query - A text string or compiled regular expression.wks
# wks.findall(query)
# wks.get_all_records() # Returns a list of dictionaries
# See https://gspread.readthedocs.io/en/latest/#gspread.models.Worksheet.range
# range(*args, **kwargs) # Returns a list of Cell objects from a specified range.
# wks.title # Title of a worksheet
# update_acell(lable, value)
# update_cell(row, col, value)
# update_title(title)
