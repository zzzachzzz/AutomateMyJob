from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from pprint import pprint
import time
import re


class Job:
    def __init__(self, marsha='MCOSI', instance='01'):
        self.driver = None  # Selenium driver
        self.e = None  # Selected element
        self.marsha = marsha
        self.instance = instance
        self.marsha_location = { 'nth-child': 0, 'page': 0 }  # Location in WEM folders
        print("Job instance created")
    
    def launch(self):
        self.driver = webdriver.Firefox()
        self.driver.get('file:///D:/Users/Zach/Google%20Drive/haha/4OpenText%20Web%20Experience%20Management.htm')
        self.actionChains = ActionChains(self.driver)

    def login(self):
        with open('creds.json', 'r') as file:
            creds = json.load(file)
        elem = driver.find_element_by_css_selector('#vui-login-name-inputEl')
        elem.send_keys(creds['user'])
        elem = driver.find_element_by_css_selector('#vui-login-pass-inputEl')
        elem.send_keys(creds['pass'])
        elem = driver.find_element_by_css_selector('#vui-login-link-submit-btnEl')
        elem.click()

    def edit_quick_actions(self):
        # Check if by_id vui-workspace-ribbon-quickaction has class vui-ribbon-selected
        self.e = self.driver.find_element_by_id('vui-workspace-ribbon-quickaction')
        if not (re.search(r'.*(vui-ribbon-selected).*', self.e.get_attribute('class'))):
            self.e.click()
        # don't target li:nth-child(x) where x in { 6, 8, 11 } C, D, E articles
        for i in range(1, 13):
            if i in {6, 8, 11}:  # C, D, E articles
                continue
            self.e = self.driver.find_element_by_css_selector(
                         '#vui-workspace-drawer-new-quickaction > ul > li:nth-child('+ str(i) +') > div > a')
            # actionChains.context_click(self.e).move_by_offset(10, -10).perform()
            actionChains.context_click(self.e)
            # self.e = self.driver.find_element_by_css_selector( Quick Action Context Menu )
            actionChains.click(self.e).perform()
            # Quick Action popup window scrolling
            self.driver.execute_script("arguments[0].scrollTop = arguments[1];", self.driver.find_element_by_id("vui-vcm-quickaction-body"), 500)
            # Remove Categories
            categories = self.driver.find_element_by_css_selector(
                             'div.x-grid-view.vui-quickaction-category-grid-scroll.x-fit-item.x-grid-view-default.x-unselectable'
                             ).find_element_by_css_selector('table > tbody'
                             ).find_elements_by_tag_name('tr')  # Last call returns list of elements
            for i in range(2, len(categories)):  # First element is a header
                cell = categories[i].find_element_by_css_selector('td.x-grid-cell-last')
                if (re.search(r'^[\s]*[A-Z]{5}[\s]*$', cell.text) or  # If a marsha tag
                    re.search(r'^[\s]*0{1}[0-9]{1}[\s]*$', cell.text)):  # If an instance tag
                    # Click checkbox for cell removal
                    categories[i].find_element_by_css_selector('td.x-grid-cell-first > div > div').click()
            # Click Remove Categories
            self.driver.find_element_by_css_selector(
                '#vui-quickaction-grid-button-category-dissociate-btnEl').click()
            # Click Add Categories
            self.driver.find_element_by_css_selector(
                '#vui-quickaction-grid-button-category-associate-btnEl').click()
            self.find_marsha()
        # endfor


    def find_marsha(self, marsha, page=1):
        if self.marsha_location['nth-child'] == True:  # Marsha already located and 'M' folder should be showing, go directly to nth-child and page
            pass #
        # Check if 'M' folder is selected
        # If not, navigate to folder
        tbody = self.driver.find_element_by_css_selector(
                         'div.x-panel.vui-grid.vui-grid-content.vui-picker-grid.x-grid-with-row-lines.x-fit-item.x-panel-default-framed.x-grid'
                     ).find_element_by_css_selector('tbody')
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

    # Alias method for ease in terminal
    def find_e(self, element):
        return self.driver.find_element_by_css_selector(element)


# 'Displaying 1 - 200 of 807'

# pprint(dir(e.job))

# 2 - 201 | first - last
# IMPORTANT. USE FOR FINDING TBODY LIST OF MARSHAS
"""
>>> e1 = job.driver.find_element_by_css_selector('div.x-panel.vui-grid.vui-grid-content.vui-picker-grid.x-grid-with-row-lines.x-fit-item.x-panel-default-framed.x-grid')
>>> tbody = e1.find_element_by_css_selector('tbody')
>>> tbody.find_element_by_css_selector('tr:nth-child(201) > td:nth-child(2) > div > div').text
'MCOSI'
>>> tbody.find_element_by_css_selector('tr:nth-child(2) > td:nth-child(2) > div > div').text
'KMGFI'
>>>
"""

# x-toolbar-text.x-box-item.x-toolbar-item.x-toolbar-text-default

# Used for finding number of results
# display = job.driver.find_elements_by_xpath('//div[starts-with(text(), "Displaying")]')

# Time it
# start_time = time.clock()
# print("{}".format(time.clock() - start_time))