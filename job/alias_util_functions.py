from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from job.run import driver, wait

"""
Alias methods for shortened name
CSS_SELECTOR, XPATH, CLASS_NAME, ID,
LINK_TEXT, NAME, PARTIAL_LINK_TEXT, TAG_NAME
"""

def find_e(selector, by=By.CSS_SELECTOR):
    return driver.find_element(by, selector)


def find_e_wait(selector, by=By.CSS_SELECTOR):
    return wait.until(EC.presence_of_element_located((by, selector) ))


def find_all_e(selector, by=By.CSS_SELECTOR):
    return driver.find_elements(by, selector)


def find_all_e_wait(selector, by=By.CSS_SELECTOR):
    return wait.until(EC.presence_of_all_elements_located((by, selector) ))


def k():
    print('ko')
