from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pprint import pprint
import colorama
from colorama import Fore, Back, Style
import logging
import json
import time
import re
from typing import List
from job.run import driver, wait
from job.alias_util_functions import find_e, find_e_wait, find_all_e, find_all_e_wait
from job import tagging_paths
from job import marsha, sheet_title


def login():
    with open('job/creds.json', 'r') as file:
        creds = json.load(file)
    e = find_e('#vui-login-name-inputEl')
    e.send_keys(creds['user'])
    e = find_e('#vui-login-pass-inputEl')
    e.send_keys(creds['pass'])
    e = find_e('#vui-login-link-submit-btnEl')
    e.click()


# Build.base_tags should be passed in
def edit_quick_actions(categories_needed: List[List[str]]) -> None:
    # Check if Quick Action bar is expanded
    e = find_e('#vui-workspace-ribbon-quickaction')
    if not (re.search(r'.*(vui-ribbon-selected).*', e.get_attribute('class'))):
        e.click()
    all_quick_actions = find_e_wait('#vui-workspace-drawer-new-quickaction > ul').text.split('\n')

    indices_of_qa_to_edit = [all_quick_actions.index(qa)+1 for qa in all_quick_actions \
                             if (re.search(r'^0[0-9]{2}', qa) and re.search(r'\[M\]', qa) )]

    for i in indices_of_qa_to_edit:
        # Scroll to quick action, right click it, and select first option with KeyDown and Enter
        e = find_e('#vui-workspace-drawer-new-quickaction > ul > li:nth-child('+str(i)+')')
        driver.execute_script("arguments[0].scrollIntoView(true);", e)
        ActionChains(driver).context_click(e).perform()
        time.sleep(0.5)
        ActionChains(driver).send_keys(Keys.DOWN, Keys.ENTER).perform()

        # Click Advanced Settings
        find_e_wait('#vui-wizard-quickaction-advancedsettings-legendTitle').click()
        
        # Scroll to bottom of Quick Action popup window
        driver.execute_script("arguments[0].scrollTop = arguments[1];", find_e("#vui-vcm-quickaction-body"), 1000)

        # Remove Categories
        categories_present = find_e(
            'div.x-grid-view.vui-quickaction-category-grid-scroll.x-fit-item' + \
            '.x-grid-view-default.x-unselectable > table > tbody'
            ).find_elements_by_tag_name('tr')  # List of web elements

        # Categories already present will be popped from categories_to_add
        categories_to_add = categories_needed
        for i in range(1, len(categories_present)):  # First element is a header
            cell = categories_present[i].find_element_by_css_selector('td.x-grid-cell-last')
            # Check if a needed category is already present
            if cell.text in [category[-1] for category in categories_needed]:
                categories_needed.pop(index(cell.text))
            else:
                # Click checkbox for category removal
                categories_present[i].find_element_by_css_selector('td.x-grid-cell-first > div > div'
                    ).click()

        # Click Remove Categories
        find_e('#vui-quickaction-grid-button-category-dissociate-btnEl').click()
        
        # Add categories
        for category in categories_to_add:
            # Click Add Categories
            find_e_wait('#vui-quickaction-grid-button-category-associate-btnEl').click()
            navigate_to_directory_in_sidebar(category)
            add_category_from_results(category[-1])

        # TODO CLICK SAVE TO SAVE QUICK ACTION AND CLOSE POPUP WINDOW

    # Done modifying quick actions
    return


def edit_qa_helper():
    tp = tagging_paths.TaggingPaths(sheet_title, marsha)

    edit_quick_actions(tp.base_tags)


# Binary search a list of web element objects for an item
# as a string, with a selector for the item's text.
def binary_search_web_element_list(arr: list, start: int, end: int,
                                   selector_for_item: tuple, item: str) -> int:
    # If last element string is less than item string, item won't be in list.
    if arr[end].find_element(*selector_for_item).text < item:
        return -1  # Element was not present

    while start <= end:
        mid = (start + end) // 2
        mid_element_text = arr[mid].find_element(*selector_for_item).text
        if mid_element_text == item:
            return mid
        elif mid_element_text < item:
            start = mid + 1
        else:
            end = mid - 1
    return -1  # Element was not present
# binary_search_web_element_list(arr, 1, len(arr)-1, item)


# Find and add category from results
def add_category_from_results(item: str) -> int:
    xpath_to_all_tr = '//div[@class="x-panel-body x-grid-body' + \
        ' x-panel-body-default-framed x-panel-body-default-framed x-layout-fit"]' + \
        '[contains(@id, "vui-vcm-ui-picker-")]//div//table//tbody//tr'

    all_tr = WebDriverWait(driver, 40).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath_to_all_tr) ))

    index_of_item = binary_search_web_element_list(all_tr, 1, len(all_tr)-1,
        (By.CSS_SELECTOR, 'td:nth-child(2)'), item)

    if index_of_item != -1:  # Item found
        all_tr[index_of_item].find_element_by_css_selector('td:nth-child(1) > div > div').click()
        # Click Add to Selection
        find_e('//span[contains(@id, "-category-button-add-btnInnerEl")]' + \
            '[text()="Add to Selections"]', by=By.XPATH).click()
        # Reset sidebar navigation
        click_all_categories_btn()
        # Click OK
        find_e('//span[contains(@id, "-button-ok-btnInnerEl")]', by=By.XPATH
            ).click()
        return None
        # return index_of_item

    if is_last_page_of_results():  # If on last page of results
        return -1
    else:  # Click next page button and check results again
        driver.find_elements_by_xpath('//button[@data-qtip="Next Page"]')[1].click()
        loading_id = driver.find_elements(By.XPATH,  # For targeting Loading dialog
            '//div[@class="x-mask-msg vui-loadmask x-layer x-mask-msg-default"]'
            )[1].get_attribute('id')
        WebDriverWait(driver, 30).until(  # Wait for Loading dialog to appear
            EC.visibility_of_element_located((By.ID, loading_id) ))
        WebDriverWait(driver, 30).until(  # Wait for Loading dialog to disappear
            EC.invisibility_of_element_located((By.ID, loading_id) ))
        # Run again on next page of results
        add_category_from_results(item)


def get_curr_page_num() -> int:
    results = driver.find_elements_by_xpath(
        '//div[starts-with(text(), "Displaying")][starts-with(@id, "tbtext-")]')[1].text
    results_begin = int(re.search(r'(?<=ing ).*(?= -)', results).group())
    results_end = int(re.search(r'(?<=- ).*(?= of)', results).group())
    current_page = results_begin // (
        results_end - results_begin + 1) + 1
    return current_page


def is_last_page_of_results() -> bool:
    results = driver.find_elements_by_xpath(
        '//div[starts-with(text(), "Displaying")][starts-with(@id, "tbtext-")]')[1].text
    results_end = int(re.search(r'(?<=- ).*(?= of)', results).group())
    results_total = int(re.search(r'(?<=of ).+', results).group())
    return results_total == results_end


def navigate_to_directory_in_sidebar(directory_path: List[str]) -> None:
    all_tr_xpath = (  # Sidebar "Category Tree"
        '//div[@class="x-panel-body x-grid-body x-panel-body-default x-panel-body-default x-layout-fit"]' + \
        '[starts-with(@id, "vui-vcm-ui-picker-")]//div//table//tbody//tr')
    all_tr = find_all_e(all_tr_xpath, By.XPATH)
    start, end = 2, len(all_tr)-1
    for directory in directory_path:
        index_of_directory = binary_search_web_element_list(
            all_tr, start, end, (By.CSS_SELECTOR, 'td > div'), directory)

        # If list item is second to last in the list
        if directory_path.index(directory) == len(directory_path)-2:
            e = all_tr[index_of_directory].find_element(By.CSS_SELECTOR, 'td > div')
            e.click()
            return

        e = all_tr[index_of_directory].find_elements(
            By.CSS_SELECTOR, 'td > div > img')[-2]
        e.click()

        prev_all_tr_length = len(all_tr)-1
        # Custom wait function
        all_tr = wait.until(nodes_have_been_added((By.XPATH, all_tr_xpath),
                                         prev_all_tr_length))
        time.sleep(2)  # Possibly change poll time for custom wait function to 1 sec
        start = index_of_directory + 1
        end = len(all_tr)-1 - prev_all_tr_length + index_of_directory


    # Upon clicking category, element is detached from DOM. Selector below necessary before another click
    all_categories_expand = all_tr.find_element_by_css_selector('tr:nth-child(2) > td > div')
    all_categories_expand.click() # Sometimes click does not register even when scrolled into view :thinking: ...
    # Best to enter "Select Categories" at root directory "All Categories" ... collapse upon closing
    # When clicking "All Categories" to collapse, must click text, not the "-/+" img


# Custom wait condition waits for number of nodes to increase
class nodes_have_been_added:
    def __init__(self, locator, prev_length):
        self.locator = locator
        self.prev_length = prev_length

    def __call__(self, driver):
        elements = driver.find_elements(*self.locator)
        if len(elements)-1 > self.prev_length:
            self.prev_length = len(elements)-1
            print(self.prev_length)
            elements = wait.until(EC.presence_of_all_elements_located(self.locator))
            print(len(elements)-1)
            if len(elements)-1 == self.prev_length:
                return elements
        else:
            return False

def got_em(cp):
    # cp = ['MARSHA Codes', 'N', 'NYCHW']
    navigate_to_directory_in_sidebar(cp)
    wait_for_loading_dialog()
    add_category_from_results(cp[-1])

    click_all_categories_btn()  # To reset sidebar navigation
    find_e('//span[contains(@id, "-button-ok-btnInnerEl")]', by=By.XPATH
        ).click()  # Click OK

def wait_for_loading_dialog():
    try:
        loading_id = driver.find_elements(By.XPATH,  # For targeting Loading dialog
            '//div[@class="x-mask-msg vui-loadmask x-layer x-mask-msg-default"]'
            )[1].get_attribute('id')
        WebDriverWait(driver, 7).until(  # Wait for Loading dialog to appear
            EC.visibility_of_element_located((By.ID, loading_id) ))
        WebDriverWait(driver, 30).until(  # Wait for Loading dialog to disappear
            EC.invisibility_of_element_located((By.ID, loading_id) ))
    except(TimeoutException, IndexError):
        print("No loading dialog found")

def click_all_categories_btn():
    all_categories_button_xpath = (  # Sidebar "Category Tree"
        '//div[@class="x-panel-body x-grid-body x-panel-body-default x-panel-body-default x-layout-fit"]' + \
        '[starts-with(@id, "vui-vcm-ui-picker-")]//div//table//tbody//tr[position()=2]//td//div')
    find_e(all_categories_button_xpath, By.XPATH
        ).click()

