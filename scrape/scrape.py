import requests
from bs4 import BeautifulSoup
import re
import pprint


# marsha = ''
# marsha = input('Enter Marsha: ')
# while not re.search(r'[A-Z]{5}', marsha, re.I):
# 	print("Invalid Marsha")
# 	marsha = input('Enter Marsha: ')
class Scrape:
	def __init__(self):
		marsha = 'tpasi'
		url = 'http://hws-test1.mi-devtest.marriott.com/hotels/fact-sheet/feature-1/' + marsha
		page = requests.get(url, timeout=25)
		self.soup = BeautifulSoup(page.content, 'html.parser')
		self.e = self.soup.select_one('#main-body-wrapper > div:nth-of-type(2)')  # All WEM content
		print(len(self.e))
		# print(soup.prettify())
