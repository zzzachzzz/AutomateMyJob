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


class Job:
    def __init__(self, marsha='SFONW'):
        self.marsha = marsha.upper()
        self.marsha_location = { 'nth-child': 0, 'page': 0 }  # Location in WEM folders
        colorama.init(autoreset=True)
        print("Job instance created")

    def login(self):
        with open('creds.json', 'r') as file:
            creds = json.load(file)
        e = self.find_e('#vui-login-name-inputEl')
        e.send_keys(creds['user'])
        e = self.find_e('#vui-login-pass-inputEl')
        e.send_keys(creds['pass'])
        e = self.find_e('#vui-login-link-submit-btnEl')
        e.click()

    def get_vcmid(self):
        tbody = self.find_e('#vui-workspace-grid-body > div > table > tbody')
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
            # wait.until(EC.frame_to_be_available_and_switch_to_it(self.find_e('iframe')))
            driver.switch_to.frame(
                    wait.until(EC.presence_of_element_located((By.TAG_NAME,'iframe') )))
            e = self.find_e_wait('html > body > textarea')
            text = e.text
            driver.switch_to.default_content()
            self.find_e('#vui-view-contentitem-window_header-targetEl > div:nth-child(4) > img').click()  # Close popup
            print(Back.CYAN + re.search(r'(?<=<VignVCMId>).*(?=</VignVCMId)', text).group())

    # For fixing "stale" content
    def stale(self):
        tbody = self.find_e('#vui-workspace-grid-body > div > table > tbody')
        tr_child_len = len(tbody.find_elements_by_tag_name('tr'))
        for i in range(2, tr_child_len+1):
            # tbody = self.find_e('#vui-workspace-grid-body > div > table > tbody')

            tbody = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#vui-workspace-grid-body > div > table > tbody') ))
            e = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td:nth-child(2) > div > ul > li:nth-child(1)')  # Pencil edit btn
            e.click()
            e = self.find_e_wait('table.x-field.vui-widget-input-text.vui-field-large.x-form-item.x-field-default')
            e = self.find_e('table.x-field.vui-widget-input-text.vui-field-large.x-form-item.x-field-default')
            e = e.find_element_by_tag_name('input')
            e.send_keys('x')
            e = driver.find_element_by_xpath('//button[@title="Save all pending changes."]')
            e.click()
            # Wait for reload caused by clicking Save
            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@title="Save all pending changes and close this window."]') ))
            time.sleep(2)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@title="Save all pending changes and close this window."]') ))
            e = self.find_e('table.x-field.vui-widget-input-text.vui-field-large.x-form-item.x-field-default')
            e = e.find_element_by_tag_name('input')
            e.send_keys(Keys.BACKSPACE)
            e = wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@title="Save all pending changes and close this window."]') ))
            e.click()

    # Future
    def translate(self):
        pass
        # tbody = self.find_e('#vui-workspace-grid-body > div > table > tbody')
        # tr_child_len = len(tbody.find_elements_by_tag_name('tr'))
        # for i in range(2, tr_child_len+1):
        #     tbody = self.find_e('#vui-workspace-grid-body > div > table > tbody')

        #     name = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td:nth-child(3) > div > div').text
        #     type_ = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td:nth-child(7) > div').text
        #     if re.search(C.trash, name, re.I) or re.search(r'ADT Wrapper', type_, re.I):  # If trashed item or wrapper type
        #         continue
        #     e = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td:nth-child(1) > div > div')  # Checkbox
        #     e.click()  # Click Checkbox

        # driver.find_element_by_id('vui-wizard-startworkflow-name-input').send_keys('wow')
        # e = self.find_e('table.x-field.vui-widget-input-text.vui-field-large.x-form-item.x-field-default')
        # e = e.find_element_by_tag_name('input')
        # e.send_keys('x')
        # e = driver.find_element_by_xpath('//button[@title="Save all pending changes."]')
        # e.click()
        # e = self.find_e('table.x-field.vui-widget-input-text.vui-field-large.x-form-item.x-field-default')
        # e = e.find_element_by_tag_name('input')
        # e.send_keys(Keys.BACKSPACE)
        # e = driver.find_element_by_xpath('//button[@title="Save all pending changes and close this window."]')
        # e.click()

    def get_expected_tags(self, name):  # Returns a set
        tile = re.search(r'((?<=Tile)|(?<=Type)|(?<=TITLE))[A-Z]', name, re.I)
        if tile:
            tile = 'Tile ' + tile.group()
        if re.search(C.trash, name, re.I) or re.search(C.article, name, re.I):
            return set()  # No tags expected
        for k, v in C.content.items():
            # print(k, v)
            if re.search(v['regex'], name, re.I):
                if k in {'skittle_backlink', 'skittle_meta', 'skittle_hero', 'skittle_B'}:
                    return {v['tag'], self.marsha, self.instance}
                elif k in {'header_C', 'header_E'}:
                    return {v['tag'], tile, self.marsha, self.instance}
                elif k in {'skittle_C', 'skittle_D', 'skittle_E'}:
                    if re.search(C.wrapper_tile, name, re.I):
                        if re.search(C.article, name, re.I):  # Is Article
                            return set()
                        else:  # Is Wrapper
                            return {tile, self.marsha, self.instance}
        print(Back.CYAN+"Made it through the loop??? Ok")
        return set()


    def has_general_description(self, name):
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


    def check_formatting(self):
        tbody = self.find_e('#vui-workspace-grid-body > div > table > tbody')
        tr_child_len = len(tbody.find_elements_by_tag_name('tr'))
        for i in range(2, tr_child_len+1):
            e = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td:nth-child(3) > div > div')
            name = e.text
            e.click()  # Only clicks to highlight current item, doesn't affect function execution
            if self.has_general_description(name):
                e = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td:nth-child(2) > div > ul > li:nth-child(4)')  # View Item button
                e.click()
                driver.switch_to.frame(
                        wait.until(EC.presence_of_element_located((By.TAG_NAME,'iframe') )))
                text = self.find_e_wait('html > body > textarea').text
                driver.switch_to.default_content()
                self.find_e('#vui-view-contentitem-window_header-targetEl > div:nth-child(4) > img').click()  # Close popup
                if re.search(r'font', text):
                    print(Back.RED+Style.BRIGHT+"Formatting found on {}".format(name))
                else:
                    print(Back.CYAN+"{} is clear of formatting".format(name))
            else:
                print(Back.CYAN+"No general description  for {}".format(name))


    def check_tags(self, marsha, instance):
        self.marsha = marsha
        self.instance = instance
        # e = self.find_e('#vui-workspace-grid-body > div > table > tbody > tr:nth-child('+str(i)+')')
        tbody = self.find_e('#vui-workspace-grid-body > div > table > tbody')
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
            expected_tags = self.get_expected_tags(name)  # Returns set
            # print(expected_tags)
            # Menu bar "Overview, Translations, Publishing, Channels, Categories, etc"
            categories_tab = self.find_e('div.x-tab-bar-body.x-tab-bar-body-top.x-tab-bar-body-default-top.x-tab-bar-body-horizontal.x-tab-bar-body-default-horizontal.x-tab-bar-body-default.x-tab-bar-body-default-top.x-tab-bar-body-default-horizontal.x-tab-bar-body-default-docked-top.x-box-layout-ct'
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

            self.find_e('img.x-tool-close').click()  # Close popup
            print("-------------------------------")
        return


    def edit_quick_actions(self):
        # Check if Quick Action bar is expanded (selected)
        e = self.find_e('#vui-workspace-ribbon-quickaction')
        if not (re.search(r'.*(vui-ribbon-selected).*', e.get_attribute('class'))):
            e.click()
        all_quick_actions = self.find_e_wait('#vui-workspace-drawer-new-quickaction > ul').text.split('\n')
        indices_of_qa_to_edit = [all_quick_actions.index(qa)+1 for qa in all_quick_actions \
                                 if (re.search(r'^IPP', qa) and not re.search(r'[CDE] Article', qa) )]

        for i in indices_of_qa_to_edit:
            # Scroll to quick action, right click it, and select first option with KeyDown and Enter
            e = self.find_e('#vui-workspace-drawer-new-quickaction > ul > li:nth-child('+str(i)+')')
            driver.execute_script("arguments[0].scrollIntoView(true);", e)
            ActionChains(driver).context_click(e).perform()
            time.sleep(0.5)
            ActionChains(driver).send_keys(Keys.DOWN, Keys.ENTER).perform()
            # End of block
            self.find_e_wait('#vui-wizard-quickaction-advancedsettings-legendTitle').click()
            
            # Quick Action popup window scroll to bottom
            driver.execute_script("arguments[0].scrollTop = arguments[1];", self.find_e("#vui-vcm-quickaction-body"), 1000)
            # Remove Categories
            categories = self.find_e(
                    'div.x-grid-view.vui-quickaction-category-grid-scroll.x-fit-item' + \
                    '.x-grid-view-default.x-unselectable > table > tbody'
                    ).find_elements_by_tag_name('tr')  # List of elements
            for i in range(2, len(categories)):  # First element is a header
                cell = categories[i].find_element_by_css_selector('td.x-grid-cell-last')
                if (re.search(r'^[\s]*[A-Z]{5}[\s]*$', cell.text, re.I) or  # If a marsha tag
                    re.search(r'^[\s]*0{1}[0-9]{1}[\s]*$', cell.text, re.I)):  # If an instance tag
                    # Click checkbox for cell removal
                    categories[i].find_element_by_css_selector('td.x-grid-cell-first > div > div').click()
            # Click Remove Categories
            self.find_e('#vui-quickaction-grid-button-category-dissociate-btnEl').click()
            # Click Add Categories
            self.find_e('#vui-quickaction-grid-button-category-associate-btnEl').click()
            # self.find_marsha(self.marsha)

            if self.marsha_location['nth-child'] != 0:  # Marsha folder located
                self.add_marsha()
            # Check location again. If add_marsha() failed, value is set back to zero.
            if self.marsha_location['nth-child'] == 0:
                self.find_marsha()
                self.add_marsha()

            print("Sleeping... for 3 minutes")
            return
            time.sleep(180)
        # endfor

    def add_marsha(self):
        # self.marsha = 'SACAK'
        # self.marsha_location['page'] = 1
        # self.marsha_location['nth-child'] = 2

        xpath_to_tbody = '//div[@class="x-panel-body x-grid-body' + \
                ' x-panel-body-default-framed x-panel-body-default-framed x-layout-fit"]' + \
                '[contains(@id, "vui-vcm-ui-picker-")]//div//table//tbody'
        # Wait for folders to load
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, xpath_to_tbody+'//tr[position()=2]') ))
        self.get_displaying_results_info()
        if self.marsha_location['page'] != self.current_page:  # Navigate to page containing marsha
        # if self.marsha_location['page'] != 1:  # Navigate to page containing marsha
            xpath_page_input = '//input[@name="inputItem"][contains(@class, "x-form-field x-form-text")]'
            self.find_e(xpath_page_input, by=By.XPATH).send_keys(Keys.ENTER)
            self.find_e(xpath_page_input, by=By.XPATH).send_keys(
                    Keys.BACKSPACE + str(self.marsha_location['page']) + Keys.ENTER)
            loading_id = driver.find_elements(By.XPATH,  # For targeting Loading dialog
                    '//div[@class="x-mask-msg vui-loadmask x-layer x-mask-msg-default"]'
                    )[1].get_attribute('id')
            WebDriverWait(driver, 30).until(  # Wait for Loading dialog to appear
                    EC.visibility_of_element_located((By.ID, loading_id) ))
            WebDriverWait(driver, 30).until(  # Wait for Loading dialog to disappear
                    EC.invisibility_of_element_located((By.ID, loading_id) ))
        tbody = self.find_e_wait(xpath_to_tbody, by=By.XPATH)
        e = tbody.find_element_by_css_selector('tr:nth-child(' + \
                str(self.marsha_location['nth-child']) + \
                ') > td:nth-child(2) > div > div')
        if e.text == self.marsha:
            tbody.find_element_by_css_selector('tr:nth-child(' + \
                    str(self.marsha_location['nth-child']) + \
                    ') > td:nth-child(1) > div > div').click()
            # Click Add to Selections
            self.find_e('//span[contains(@id, "-category-button-add-btnInnerEl")]' + \
                    '[text()="Add to Selections"]', by=By.XPATH).click()
            # Click OK
            self.find_e('//span[contains(@id, "-button-ok-btnInnerEl")]',
                    by=By.XPATH).click()
            return True
        else:  # If the location moved, it will need to be found again
            self.marsha_location['nth-child'] = 0
            self.marsha_location['page'] = 0
            # TODO
            # Close categories to prepare for find_marsha, or return to page 1
            return False

    def find_marsha(self, page=1):
        xpath_to_tbody = '//div[@class="x-panel-body x-grid-body' + \
                ' x-panel-body-default-framed x-panel-body-default-framed x-layout-fit"]' + \
                '[contains(@id, "vui-vcm-ui-picker-")]//div//table//tbody'
        # Marsha already located and 'M' folder should be showing, go directly to nth-child and page
        # Check if 'M' folder is selected
        # If not, navigate to folder
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, xpath_to_tbody+'//tr[position()=2]') ))
        self.get_displaying_results_info()
        end = 200 if self.results_end % 200 == 0 else self.results_end % 200
        tbody = self.find_e_wait(xpath_to_tbody, by=By.XPATH)
        # Get text of last result shown and compare alphabetically
        last_result_shown = tbody.find_element_by_css_selector('tr:nth-child(' + str(end+1) + ') > td:nth-child(2) > div > div')
        if self.marsha <= last_result_shown.text:
            for n in range(2, end+2):
                e = tbody.find_element_by_css_selector('tr:nth-child(' + str(n) + ') > td:nth-child(2) > div > div')
                if e.text == self.marsha:
                    tbody.find_element_by_css_selector('tr:nth-child(' + str(n) + ') > td:nth-child(1) > div > div').click()
                    self.marsha_location['nth-child'] = n
                    self.marsha_location['page'] = page
                    return True
            return False  # Rare failure, missing folder
        else:
            if self.results_total == self.results_end:  # If on last page of results
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
            self.find_marsha(page)

    def get_displaying_results_info(self):
        results = driver.find_elements_by_xpath('//div[starts-with(text(), "Displaying")]')[1].text
        print(results)
        # 'Displaying 1 - 200 of 807'
        self.results_begin = int(re.search(r'(?<=ing ).*(?= -)', results).group())  # 1
        self.results_end = int(re.search(r'(?<=- ).*(?= of)', results).group())  # 200
        self.results_total = int(re.search(r'(?<=of ).+', results).group())  # 807
        self.current_page = self.results_begin // (
                self.results_end - self.results_begin + 1) + 1

    # Alias methods for shortened name
    # CSS_SELECTOR, XPATH, CLASS_NAME, ID,
    # LINK_TEXT, NAME, PARTIAL_LINK_TEXT, TAG_NAME
    def find_e(self, element, by=By.CSS_SELECTOR):
        return driver.find_element(by, element)

    def find_e_wait(self, element, by=By.CSS_SELECTOR):
        return wait.until(EC.presence_of_element_located((by, element) ))
