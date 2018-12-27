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
    options = webdriver.ChromeOptions()
    options.add_argument('user-data-dir=C:\\Local\\selenium_chrome_profile')
    options.add_argument('--disable-infobars')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    path = 'C:\\Local\\chromedriver_win32\\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=path, chrome_options=options)
wait = webdriver.support.ui.WebDriverWait(driver, 10)

# Imports dependent on driver and wait
from job.alias_util_functions import find_e, find_e_wait, find_all_e, find_all_e_wait, k
from job import wem_scripts as w

marsha = 'TCISI'
url = 'http://wemprod.marriott.com:27110/content/#/workspace/folder/hotelwebsites/us/' + \
       marsha.lower()[0]+'/'+marsha.lower()+'/Elevated'
driver.get(url)
