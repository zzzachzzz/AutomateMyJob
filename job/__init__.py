from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pprint import pprint
from importlib import reload


use_ie = input()
if use_ie in {'ie', 'i'}:
    driver = webdriver.Ie()
else:
    driver = webdriver.Chrome()
wait = webdriver.support.ui.WebDriverWait(driver, 10)

from .alias_util_functions import find_e, find_e_wait, find_all_e, find_all_e_wait, k
from . import job
from . import build
j = job.Job()
b = build.Build()

# IPP
# marsha, instance = 'sfonw', '02'
# url = 'http://wemprod.marriott.com:27110/content/#/workspace/folder/hotelwebsites/us/' + \
#        marsha.lower()[0]+'/'+marsha.lower()+'/IPP'+instance

# T3
marsha = 'tcisi'
url = 'http://wemprod.marriott.com:27110/content/#/workspace/folder/hotelwebsites/us/' + \
       marsha.lower()[0]+'/'+marsha.lower()+'/Elevated'
driver.get(url)
