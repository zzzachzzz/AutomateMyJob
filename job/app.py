from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pprint import pprint
import colorama
from colorama import Fore, Back, Style
import logging
import json
import time
import re


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
    trash = r'^(TRASH|ZZTRASH)'
    mi = r'[A-Z]{5}_IPP[0-9]{2}'

C = Components  # Alias, shortened "import" name


class Job:
    def __init__(self, marsha='MCOSI', instance='01'):
        self.marsha = marsha
        self.instance = instance
        self.marsha_location = { 'nth-child': 0, 'page': 0 }  # Location in WEM folders
        colorama.init(autoreset=True)
        print("Job instance created")
    
    def launch(self):
        url = 'http://wemprod.marriott.com:27110/content/#/workspace/folder/hotelwebsites/us/m/myrsi/IPP03'
        self.driver = webdriver.Ie()
        self.driver.implicitly_wait(15)  # Waits 15 seconds before throwing exception
        self.driver.get(url)

    def login(self):
        with open('creds.json', 'r') as file:
            creds = json.load(file)
        e = self.find_e('#vui-login-name-inputEl')
        e.send_keys(creds['user'])
        e = self.find_e('#vui-login-pass-inputEl')
        e.send_keys(creds['pass'])
        e = self.find_e('#vui-login-link-submit-btnEl')
        e.click()

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
            e.click()
            if self.has_general_description(name):
                e = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td:nth-child(2) > div > ul > li:nth-child(4)')  # View Item button
                ac = ActionChains(self.driver)
                ac.move_to_element(e).click().perform()
                time.sleep(3)
                self.driver.switch_to.frame(self.find_e('iframe'))
                e = self.find_e('html > body > textarea')
                text = e.text
                self.driver.switch_to.default_content()
                self.find_e('#vui-view-contentitem-window_header-targetEl > div:nth-child(4) > img').click()  # Close popup
                if re.search(r'font', text):
                    print(Back.RED+Style.BRIGHT+"Formatting found on {}".format(name))
                else:
                    print(Back.CYAN+"{} is clear of formatting".format(name))
            else:
                print(Back.CYAN+"No general description  for {}".format(name))


    def verify_tags(self, marsha, instance):
        self.marsha = marsha
        self.instance = instance
        # e = self.find_e('#vui-workspace-grid-body > div > table > tbody > tr:nth-child('+str(i)+')')
        tbody = self.find_e('#vui-workspace-grid-body > div > table > tbody')
        tr_child_len = len(tbody.find_elements_by_tag_name('tr'))
        for i in range(2, tr_child_len+1):
            # Click on row before clicking on properties button to avoid unregistered clicks when out of view
            e = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td:nth-child(3) > div > div')
            e.click()
            name = e.text  # System Name
            e = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td:nth-child(2) > div > ul > li:nth-child(2)')  # Properties button
            ac = ActionChains(self.driver)
            ac.move_to_element(e).click().perform()
            print("-------------------------------")
            print(name)
            expected_tags = self.get_expected_tags(name)  # Returns set
            # print(expected_tags)
            e.click()
            # Menu bar "Overview, Translations, Publishing, Channels, Categories, etc"
            e = self.find_e('div.x-tab-bar-body.x-tab-bar-body-top.x-tab-bar-body-default-top.x-tab-bar-body-horizontal.x-tab-bar-body-default-horizontal.x-tab-bar-body-default.x-tab-bar-body-default-top.x-tab-bar-body-default-horizontal.x-tab-bar-body-default-docked-top.x-box-layout-ct')
            ### Click Categories Tab ####
            time.sleep(0.5)
            categories_tab = e.find_element_by_css_selector('div:nth-child(2) > div > div:nth-child(5) > em > button')
            categories_tab.click()
            time.sleep(2.5)
            e = self.driver.find_elements_by_xpath('//div[starts-with(@id, "CATEGORY_ASSOCIATIONS_GRID_")]')[1]
            
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

    def ok(self):
        self.actionChains = ActionChains(self.driver)
        e = self.find_e('.main > div:nth-child(1) > div:nth-child(4) > center:nth-child(1) > a:nth-child(1)')
        self.actionChains.context_click(e).perform()
        # self.actionChains.move_to_element_with_offset(e, 10, 10).context_click().perform()

    def edit_quick_actions(self):
        # Check if Quick Action bar is expanded (selected)
        e = self.driver.find_e('#vui-workspace-ribbon-quickaction')
        if not (re.search(r'.*(vui-ribbon-selected).*', e.get_attribute('class'))):
            e.click()
        for i in range(1, 13):
            if i in {6, 8, 11}:  # C, D, E articles
                continue
            actionChains = ActionChains(self.driver)
            e = self.find_e('#vui-workspace-drawer-new-quickaction > ul > li:nth-child('+ str(i) +') > div > a > span')
            actionChains.move_to_element(e).context_click().send_keys(Keys.DOWN, Keys.ENTER).perform()

            return # interrupt function

            # TODO
            # self.e = self.find_e( Quick Action Context Menu )
            self.actionChains.click(self.e).perform()
            # Quick Action popup window scrolling
            self.driver.execute_script("arguments[0].scrollTop = arguments[1];", self.find_e("#vui-vcm-quickaction-body"), 500)
            # Remove Categories
            categories = self.find_e(
                             'div.x-grid-view.vui-quickaction-category-grid-scroll.x-fit-item.x-grid-view-default.x-unselectable'
                             ).find_element_by_css_selector('table > tbody'
                             ).find_elements_by_tag_name('tr')  # Last call returns list of elements
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
            self.find_marsha()
        # endfor


    def find_marsha(self, marsha, page=1):
        if self.marsha_location['nth-child'] == True:  # Marsha already located and 'M' folder should be showing, go directly to nth-child and page
            pass #
        # Check if 'M' folder is selected
        # If not, navigate to folder
        tbody = self.find_e(
                         'div.x-panel.vui-grid.vui-grid-content.vui-picker-grid.x-grid-with-row-lines.x-fit-item.x-panel-default-framed.x-grid'
                     ).find_element_by_tag_name('tbody')
        self.get_num_results()
        end = 200 if self.results_end % 200 == 0 else self.results_end % 200
        e = tbody.find_element_by_css_selector('tr:nth-child(' + str(end+1) + ') > td:nth-child(2) > div > div')
        if marsha <= e.text:
            for n in range(2, end+2):
                e = tbody.find_element_by_css_selector('tr:nth-child(' + str(n) + ') > td:nth-child(2) > div > div')
                # return When found | self.tbody.find_element_by_css_selector('tr:nth-child(' + str(marsha+1) + ') > td:nth-child(1) > div > div').click()
                if e.text == marsha:
                    tbody.find_element_by_css_selector('tr:nth-child(' + str(n) + ') > td:nth-child(1) > div > div').click()
                    self.marsha_location['nth-child'] = n
                    self.marsha_location['page'] = page
                    return e.text
            return None  # Marsha not found
        else:
            # Click next page button and check results again
            self.driver.find_elements_by_xpath('//button[@data-qtip="Next Page"]')[1].click()
            page += 1
            self.find_marsha(marsha, page)  # Beware unregistered click
            # Add condition check for last page of results, return None if True

    def get_num_results(self):
        results = self.driver.find_elements_by_xpath('//div[starts-with(text(), "Displaying")]')[1].text
        print(results)
        # 'Displaying 1 - 200 of 807'
        self.results_begin = int(re.search(r'(?<=ing ).*(?= -)', results).group())  # 1
        self.results_end = int(re.search(r'(?<=- ).*(?= of)', results).group())  # 200
        self.results_total = int(re.search(r'(?<=of ).+', results).group())  # 807

    # Alias method for shortened method name
    def find_e(self, element, by=By.CSS_SELECTOR):
        # CSS_SELECTOR, XPATH, CLASS_NAME, ID,
        # LINK_TEXT, NAME, PARTIAL_LINK_TEXT, TAG_NAME
        if by == By.CSS_SELECTOR:
            return self.driver.find_element(By.CSS_SELECTOR, element)
        if by == By.XPATH:
            return self.driver.find_element(By.XPATH, element)
        if by == By.CLASS_NAME:
            return self.driver.find_element(By.CLASS_NAME, element)
