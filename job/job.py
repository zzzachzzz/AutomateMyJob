from selenium import webdriver
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
from . import driver, wait
from . import find_e, find_e_wait, find_all_e, find_all_e_wait


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('tagging_check.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class Components:
    content = {
        'skittle_backlink': { 'regex': r'_backToParentLink|Link', 'tag': 'textLink' },
        'skittle_meta': { 'regex': r'_meta', 'tag': 'HotelOverview' },
        'skittle_hero': { 'regex': r'_singleHeroImage', 'tag': 'singleHeroImage' },
        'skittle_B': { 'regex': r'_HotelOverview', 'tag': 'HotelOverview' },
        'skittle_C': { 'regex': r'_headingTextListOfArticles' },
        'skittle_D': { 'regex': r'_imageHeaderTextCtaAdvanced' },
        'skittle_E': { 'regex': r'_imageHeaderTextCta(?!Advanced)' },
        'header_C': { 'regex': r'_headingTextListOfArticles_TITLE[A-Z]', 'tag': 'Header' },
        'header_E': { 'regex': r'_imageHeaderTextCta_TITLE[A-Z]', 'tag': 'Header' },
    }
    wrapper_tile = r'_(Tile|Type)[A-Z]'
    article = r'_Article[0-9]{1,2}'
    trash = r'^(TRASH|ZZTRASH|DNB)'
    mi = r'[A-Z]{5}_IPP[0-9]{2}'

C = Components  # Alias, shortened "import" name


marsha = marsha.upper()
marsha_location = { 'nth-child': 0, 'page': 0 }  # Location in WEM folders
colorama.init(autoreset=True)


def login():
    with open('creds.json', 'r') as file:
        creds = json.load(file)
    e = find_e('#vui-login-name-inputEl')
    e.send_keys(creds['user'])
    e = find_e('#vui-login-pass-inputEl')
    e.send_keys(creds['pass'])
    e = find_e('#vui-login-link-submit-btnEl')
    e.click()


def get_vcmid():
    tbody = find_e('#vui-workspace-grid-body > div > table > tbody')
    tr_child_len = len(tbody.find_elements_by_tag_name('tr'))
    for i in range(2, tr_child_len+1):
        e = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td:nth-child(3) > div > div')
        name = e.text
        if re.search(C.trash, name, re.I):
            continue
        print(Back.CYAN + name)
        e.click()
        # time.sleep(2)
        e = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td:nth-child(2) > div > ul > li:nth-child(4)')  # View Item button
        e.click()
        # time.sleep(2)
        # wait.until(EC.frame_to_be_available_and_switch_to_it(find_e('iframe')))
        driver.switch_to.frame(
                wait.until(EC.presence_of_element_located((By.TAG_NAME,'iframe') )))
        e = find_e_wait('html > body > textarea')
        text = e.text
        driver.switch_to.default_content()
        find_e('#vui-view-contentitem-window_header-targetEl > div:nth-child(4) > img').click()  # Close popup
        print(Back.CYAN + re.search(r'(?<=<VignVCMId>).*(?=</VignVCMId)', text).group())


# For fixing "stale" content
def stale():
    tbody = find_e('#vui-workspace-grid-body > div > table > tbody')
    tr_child_len = len(tbody.find_elements_by_tag_name('tr'))
    for i in range(2, tr_child_len+1):
        # tbody = find_e('#vui-workspace-grid-body > div > table > tbody')
        tbody = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#vui-workspace-grid-body > div > table > tbody') ))
        e = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td:nth-child(2) > div > ul > li:nth-child(1)')  # Pencil edit btn
        e.click()
        e = find_e_wait('table.x-field.vui-widget-input-text.vui-field-large.x-form-item.x-field-default')
        e = find_e('table.x-field.vui-widget-input-text.vui-field-large.x-form-item.x-field-default')
        e = e.find_element_by_tag_name('input')
        e.send_keys('x')
        e = driver.find_element_by_xpath('//button[@title="Save all pending changes."]')
        e.click()
        # Wait for reload caused by clicking Save
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@title="Save all pending changes and close this window."]') ))
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@title="Save all pending changes and close this window."]') ))
        e = find_e('table.x-field.vui-widget-input-text.vui-field-large.x-form-item.x-field-default')
        e = e.find_element_by_tag_name('input')
        e.send_keys(Keys.BACKSPACE)
        e = wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@title="Save all pending changes and close this window."]') ))
        e.click()


def get_expected_tags(name):  # Returns a set
    tile = re.search(r'((?<=Tile)|(?<=Type)|(?<=TITLE))[A-Z]', name, re.I)
    if tile:
        tile = 'Tile ' + tile.group()
    if re.search(C.trash, name, re.I) or re.search(C.article, name, re.I):
        return set()  # No tags expected
    for k, v in C.content.items():
        # print(k, v)
        if re.search(v['regex'], name, re.I):
            if k in {'skittle_backlink', 'skittle_meta', 'skittle_hero', 'skittle_B'}:
                return {v['tag'], marsha, instance}
            elif k in {'header_C', 'header_E'}:
                return {v['tag'], tile, marsha, instance}
            elif k in {'skittle_C', 'skittle_D', 'skittle_E'}:
                if re.search(C.wrapper_tile, name, re.I):
                    if re.search(C.article, name, re.I):  # Is Article
                        return set()
                    else:  # Is Wrapper
                        return {tile, marsha, instance}
    print(Back.CYAN+"Made it through the loop??? Ok")
    return set()


def has_general_description(name):
    if re.search(C.trash, name, re.I):
        return False
    for k, v in C.content.items():
        if re.search(v['regex'], name, re.I):
            if k in {'skittle_backlink', 'skittle_meta', 'skittle_hero'}:
                return False
            elif k in {'skittle_B', 'header_C', 'header_E'}:
                return True
            elif k in {'skittle_C', 'skittle_D', 'skittle_E'}:
                if re.search(C.article, name, re.I) and re.search(C.wrapper_tile, name, re.I):
                    return True
                return False
    print(Back.CYAN+"Made it through the loop??? Ok")


def check_formatting():
    tbody = find_e('#vui-workspace-grid-body > div > table > tbody')
    tr_child_len = len(tbody.find_elements_by_tag_name('tr'))
    for i in range(2, tr_child_len+1):
        e = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td:nth-child(3) > div > div')
        name = e.text
        e.click()  # Only clicks to highlight current item, doesn't affect function execution
        if has_general_description(name):
            e = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td:nth-child(2) > div > ul > li:nth-child(4)')  # View Item button
            e.click()
            driver.switch_to.frame(
                    wait.until(EC.presence_of_element_located((By.TAG_NAME,'iframe') )))
            text = find_e_wait('html > body > textarea').text
            driver.switch_to.default_content()
            find_e('#vui-view-contentitem-window_header-targetEl > div:nth-child(4) > img').click()  # Close popup
            if re.search(r'font', text):
                print(Back.RED+Style.BRIGHT+"Formatting found on {}".format(name))
            else:
                print(Back.CYAN+"{} is clear of formatting".format(name))
        else:
            print(Back.CYAN+"No general description  for {}".format(name))


def check_tags(marsha, instance):
    marsha = marsha
    instance = instance
    # e = find_e('#vui-workspace-grid-body > div > table > tbody > tr:nth-child('+str(i)+')')
    tbody = find_e('#vui-workspace-grid-body > div > table > tbody')
    tr_child_len = len(tbody.find_elements_by_tag_name('tr'))
    for i in range(2, tr_child_len+1):
        # Click on row before clicking on properties button to avoid unregistered clicks when out of view
        e = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td:nth-child(3) > div > div')
        # e.click()
        name = e.text  # System Name
        e = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td:nth-child(2) > div > ul > li:nth-child(2)')  # Properties button
        e.click()
        print("-------------------------------")
        print(name)
        expected_tags = get_expected_tags(name)  # Returns set
        # print(expected_tags)
        # Menu bar "Overview, Translations, Publishing, Channels, Categories, etc"
        categories_tab = find_e('div.x-tab-bar-body.x-tab-bar-body-top.x-tab-bar-body-default-top.x-tab-bar-body-horizontal.x-tab-bar-body-default-horizontal.x-tab-bar-body-default.x-tab-bar-body-default-top.x-tab-bar-body-default-horizontal.x-tab-bar-body-default-docked-top.x-box-layout-ct'
                                     + ' > div:nth-child(2) > div > div:nth-child(5) > em > button')
        categories_tab.click()
        e = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, '//div[starts-with(@id, "CATEGORY_ASSOCIATIONS_GRID_")]')))[1]

        actual_tags = {s.strip() for s in e.text.split('\n')}
        actual_tags = {tag for tag in actual_tags if tag != ''}

        print("Expected: {}".format(expected_tags))
        print("Actual: {}".format(actual_tags))

        for tag in expected_tags.difference(actual_tags):
            print(Back.RED+Style.BRIGHT+'Tag expected, is missing: {}'.format(tag))

        for tag in actual_tags.difference(expected_tags):
            print(Back.RED+Style.BRIGHT+"Tag should not be present: {}".format(tag))

        find_e('img.x-tool-close').click()  # Close popup
        print("-------------------------------")


def edit_quick_actions():
    # Check if Quick Action bar is expanded (selected)
    e = find_e('#vui-workspace-ribbon-quickaction')
    if not (re.search(r'.*(vui-ribbon-selected).*', e.get_attribute('class'))):
        e.click()
    all_quick_actions = find_e_wait('#vui-workspace-drawer-new-quickaction > ul').text.split('\n')
    # indices_of_qa_to_edit = [all_quick_actions.index(qa)+1 for qa in all_quick_actions \
    #                          if (re.search(r'^IPP', qa) and not re.search(r'[CDE] Article', qa) )]
    indices_of_qa_to_edit = [all_quick_actions.index(qa)+1 for qa in all_quick_actions \
                             if (re.search(r'^0[0-9]{2}', qa) and re.search(r'\[M\]', qa) )]

    for i in indices_of_qa_to_edit:
        # Scroll to quick action, right click it, and select first option with KeyDown and Enter
        e = find_e('#vui-workspace-drawer-new-quickaction > ul > li:nth-child('+str(i)+')')
        driver.execute_script("arguments[0].scrollIntoView(true);", e)
        ActionChains(driver).context_click(e).perform()
        time.sleep(0.5)
        ActionChains(driver).send_keys(Keys.DOWN, Keys.ENTER).perform()
        # End of block
        find_e_wait('#vui-wizard-quickaction-advancedsettings-legendTitle').click()
        
        # Quick Action popup window scroll to bottom
        driver.execute_script("arguments[0].scrollTop = arguments[1];", find_e("#vui-vcm-quickaction-body"), 1000)
        # Remove Categories
        categories = find_e(
            'div.x-grid-view.vui-quickaction-category-grid-scroll.x-fit-item' + \
            '.x-grid-view-default.x-unselectable > table > tbody'
            ).find_elements_by_tag_name('tr')  # List of elements
        for i in range(1, len(categories)):  # First element is a header
            cell = categories[i].find_element_by_css_selector('td.x-grid-cell-last')
            if (re.search(r'^[\s]*[A-Z]{5}[\s]*$', cell.text, re.I) or  # If a marsha tag
                re.search(r'^[\s]*0{1}[0-9]{1}[\s]*$', cell.text, re.I)):  # If an instance tag
                # Click checkbox for cell removal
                categories[i].find_element_by_css_selector('td.x-grid-cell-first > div > div').click()
        # Click Remove Categories
        find_e('#vui-quickaction-grid-button-category-dissociate-btnEl').click()
        # Click Add Categories
        find_e('#vui-quickaction-grid-button-category-associate-btnEl').click()
        # find_marsha(marsha)

        if marsha_location['nth-child'] != 0:  # Marsha folder located
            add_category()
        # Check location again. If add_marsha() failed, value is set back to zero.
        if marsha_location['nth-child'] == 0:
            find_marsha()
            add_category()

        print("Sleeping... for 3 minutes")
        return
        time.sleep(180)
    # endfor


def add_category():
    # marsha = 'TAEMR'
    # marsha_location['page'] = 1
    # marsha_location['nth-child'] = 3

    xpath_to_tbody = '//div[@class="x-panel-body x-grid-body' + \
        ' x-panel-body-default-framed x-panel-body-default-framed x-layout-fit"]' + \
        '[contains(@id, "vui-vcm-ui-picker-")]//div//table//tbody'
    # Wait for folders to load
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, xpath_to_tbody+'//tr[position()=2]') ))
    get_displaying_results_info()
    if marsha_location['page'] != get_curr_page_num():  # Navigate to page containing marsha
        xpath_page_input = '//input[starts-with(@id, "numberfield-")][@name="inputItem"][contains(@class, "x-form-field x-form-text")]'
        page_input = driver.find_elements_by_xpath(xpath_page_input)[1]
        page_input.send_keys(Keys.ENTER)
        page_input.send_keys(
            Keys.BACKSPACE + str(marsha_location['page']) + Keys.ENTER)
        loading_id = driver.find_elements(By.XPATH,  # For targeting Loading dialog
            '//div[@class="x-mask-msg vui-loadmask x-layer x-mask-msg-default"]'
            )[1].get_attribute('id')
        WebDriverWait(driver, 30).until(  # Wait for Loading dialog to appear
            EC.visibility_of_element_located((By.ID, loading_id) ))
        WebDriverWait(driver, 30).until(  # Wait for Loading dialog to disappear
            EC.invisibility_of_element_located((By.ID, loading_id) ))
    # end of old if block
    tbody = find_e_wait(xpath_to_tbody, by=By.XPATH)
    e = tbody.find_element_by_css_selector('tr:nth-child(' + \
        str(marsha_location['nth-child']) + \
        ') > td:nth-child(2) > div > div')
    if e.text == marsha:
        tbody.find_element_by_css_selector('tr:nth-child(' + \
            str(marsha_location['nth-child']) + \
            ') > td:nth-child(1) > div > div').click()
        # Click Add to Selections
        find_e('//span[contains(@id, "-category-button-add-btnInnerEl")]' + \
            '[text()="Add to Selections"]', by=By.XPATH).click()
        # Click OK
        find_e('//span[contains(@id, "-button-ok-btnInnerEl")]',
            by=By.XPATH).click()
        return True
    else:  # If the location moved, it will need to be found again
        marsha_location['nth-child'] = 0
        marsha_location['page'] = 0
        # TODO
        # Close categories to prepare for find_marsha, or return to page 1
        return False


# Binary search a list of web element objects for an item as a string,
# with a selector for the item's text.
def binary_search_web_element_list(arr: list, start: int, end: int, selector_for_item: tuple, item: str) -> int:
    while start <= end:
        mid = start + (end - start) // 2
        mid_element_text = arr[mid].find_element(*selector_for_item).text
        # Check if category is present at mid
        if mid_element_text == category:
            return mid
        # If category is greater, ignore left half
        elif mid_element_text < category:
            start = mid + 1
        # If category is smaller, ignore right half
        else:
            end = mid - 1
    # If we reach here, then the element was not present.
    return -1
# binary_search_web_element_list(arr, 1, len(arr)-1, x)


def find_marsha(page=1):
    xpath_to_tbody = '//div[@class="x-panel-body x-grid-body' + \
        ' x-panel-body-default-framed x-panel-body-default-framed x-layout-fit"]' + \
        '[contains(@id, "vui-vcm-ui-picker-")]//div//table//tbody'
    # Marsha already located and 'M' folder should be showing, go directly to nth-child and page
    # Check if 'M' folder is selected
    # If not, navigate to folder
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, xpath_to_tbody+'//tr[position()=2]') ))
    get_displaying_results_info()
    end = 200 if results_end % 200 == 0 else results_end % 200
    tbody = find_e_wait(xpath_to_tbody, by=By.XPATH)
    # Get text of last result shown and compare alphabetically
    last_result_shown = tbody.find_element_by_css_selector('tr:nth-child(' + str(end+1) + ') > td:nth-child(2) > div > div')
    if marsha <= last_result_shown.text:
        for n in range(2, end+2):
            e = tbody.find_element_by_css_selector('tr:nth-child(' + str(n) + ') > td:nth-child(2) > div > div')
            if e.text == marsha:
                marsha_location['nth-child'] = n
                marsha_location['page'] = page
                return True
        return False  # Rare failure, missing folder
    else:
        if results_total == results_end:  # If on last page of results
            return False  # Rare failure, missing folder
        # Click next page button and check results again
        driver.find_elements_by_xpath('//button[@data-qtip="Next Page"]')[1].click()
        loading_id = driver.find_elements(By.XPATH,  # For targeting Loading dialog
            '//div[@class="x-mask-msg vui-loadmask x-layer x-mask-msg-default"]'
            )[1].get_attribute('id')
        WebDriverWait(driver, 30).until(  # Wait for Loading dialog to appear
            EC.visibility_of_element_located((By.ID, loading_id) ))
        WebDriverWait(driver, 30).until(  # Wait for Loading dialog to disappear
            EC.invisibility_of_element_located((By.ID, loading_id) ))
        page += 1
        find_marsha(page)


# Possibly deprecated due to new binary search called
# with list of table rows (tr) passed into function.
def get_displaying_results_info():
    results = driver.find_elements_by_xpath(
        '//div[starts-with(text(), "Displaying")][starts-with(@id, "tbtext-")]')[1].text
    results_begin = int(re.search(r'(?<=ing ).*(?= -)', results).group())  # 1
    results_end = int(re.search(r'(?<=- ).*(?= of)', results).group())  # 200
    results_total = int(re.search(r'(?<=of ).+', results).group())  # 807
    current_page = results_begin // (
        results_end - results_begin + 1) + 1


def get_curr_page_num():
    results = driver.find_elements_by_xpath(
        '//div[starts-with(text(), "Displaying")][starts-with(@id, "tbtext-")]')[1].text
    results_begin = int(re.search(r'(?<=ing ).*(?= -)', results).group())
    results_end = int(re.search(r'(?<=- ).*(?= of)', results).group())
    results_total = int(re.search(r'(?<=of ).+', results).group())
    current_page = results_begin // (
        results_end - results_begin + 1) + 1
    return current_page


def navigate_folders():
    tbody = find_e(  # Sidebar "Category Tree"
        '//div[@class="x-panel-body x-grid-body x-panel-body-default x-panel-body-default x-layout-fit"]' + \
        '[starts-with(@id, "vui-vcm-ui-picker-")]//div//table//tbody', By.XPATH)

    # Upon clicking category, element is detached from DOM. Selector below necessary before another click
    all_categories_expand = tbody.find_element_by_css_selector('tr:nth-child(2) > td > div')
    all_categories_expand.click() # Sometimes click does not register even when scrolled into view :thinking: ...
    # Best to enter "Select Categories" at root directory "All Categories" ... collapse upon closing
    # When clicking "All Categories" to collapse, must click text, not the "-/+" img

category_path = ['HWS Tier 3', 'Landing Page', 'A', 'heroImageHeaderTextCta']


def ok():
    curr_depth_len, start = len(tbody.find_elements_by_tag_name('tr')), 3
    for depth in category_path:
        for i in range(start, curr_depth_len):
            e = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td > div')
            if e.text == depth:
                if category_path.index(depth) == len(category_path)-1:  # If list item is the last of the list (index of -1)
                    pass
                elif category_path.index(depth) == len(category_path)-2:  # If list item is second to last (index of -2)
                    e = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td > div')
                    e.click()
                else:
                    e = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td > div > img.x-tree-elbow-plus.x-tree-expander')
                    e.click()
