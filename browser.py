from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Chrome()
browser.get('http://automatetheboringstuff.com')

elem = browser.find_element_by_css_selector('body > div.main > div:nth-child(5) > center > a:nth-child(1) > img')
print(elem.text)
print(elem.click())
input('Press Enter to exit')
browser.quit()
