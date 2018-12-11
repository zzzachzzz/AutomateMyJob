from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pprint import pprint
# import colorama
# from colorama import Fore, Back, Style
# import logging
# import json
# import time
# import re
from importlib import reload



driver = webdriver.Chrome()
# driver = webdriver.Ie()
wait = webdriver.support.ui.WebDriverWait(driver, 10)
from .alias_util_functions import find_e, find_e_wait, find_all_e, find_all_e_wait, k
from . import job
from . import build
j = job.Job()
b = build.Build()
marsha, instance = 'sfonw', '02'
url = 'http://wemprod.marriott.com:27110/content/#/workspace/folder/hotelwebsites/us/' + \
       marsha.lower()[0]+'/'+marsha.lower()+'/IPP'+instance
driver.get(url)
