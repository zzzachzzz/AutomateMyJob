from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

window1 = webdriver.Firefox()
window1.get('https://www.python.org')

elem = window1.find_element_by_css_selector('#id-search-field')
# Keys.RETURN needed instead of elem.submit() for Firefox?
elem.send_keys('cute pics of dogs' + Keys.RETURN)
# elem.submit()

# print(elem.text)
# print(elem.click())
input('Press Enter to exit')
window1.quit()
