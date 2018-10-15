from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pprint import pprint
import time
import re


class Job:
    def __init__(self):
        self.driver = None  # Selenium driver
        self.e = None  # Selected element
        print("Job instance created")
    
    def launch(self):
        self.driver = webdriver.Firefox()
        self.driver.get('http://wemprod.marriott.com:27110/content/#/workspace/folder/hotelwebsites/us/b/bosbo/IPP 05')

    def login(self):
        with open('creds.json', 'r') as file:
            creds = json.load(file)
        elem = driver.find_element_by_css_selector('#vui-login-name-inputEl')
        elem.send_keys(creds['user'])
        elem = driver.find_element_by_css_selector('#vui-login-pass-inputEl')
        elem.send_keys(creds['pass'])
        elem = driver.find_element_by_css_selector('#vui-login-link-submit-btnEl')
        elem.click()

    def edit_quick_action(self, q_action):
        qa_targets = {'backlink': '#vui-workspace-drawer-new-quickaction > ul > li:nth-child(1) > div > a'}
        # Needs to check quick actions tab is open
        self.e = self.driver.find_element_by_css_selector(qa_targets[q_action]).click()
        # Edit Quick Action popup window scrolling
        self.driver.execute_script("arguments[0].scrollTop = arguments[1];", self.driver.find_element_by_id("vui-vcm-quickaction-body"), 500)

    def find_marsha(self, marsha):
        self.tbody = self.driver.find_element_by_css_selector(
                         'div.x-panel.vui-grid.vui-grid-content.vui-picker-grid.x-grid-with-row-lines.x-fit-item.x-panel-default-framed.x-grid'
                     ).find_element_by_css_selector('tbody')
        self.get_num_results()
        end = 200 if self.results_end % 200 == 0 else self.results_end % 200
        self.e = self.tbody.find_element_by_css_selector('tr:nth-child(' + str(end+1) + ') > td:nth-child(2) > div > div')
        if marsha <= self.e.text:
            for i in range(1, end+1):
                self.e = self.tbody.find_element_by_css_selector('tr:nth-child(' + str(i+1) + ') > td:nth-child(2) > div > div')
                # return When found | self.tbody.find_element_by_css_selector('tr:nth-child(' + str(marsha+1) + ') > td:nth-child(1) > div > div').click()
                if self.e.text == marsha:
                    self.tbody.find_element_by_css_selector('tr:nth-child(' + str(i+1) + ') > td:nth-child(1) > div > div').click()
                    return self.e.text
            return None  # Marsha not found
        else:
            # Click next page button and check results again
            self.driver.find_elements_by_xpath('//button[@data-qtip="Next Page"]')[1].click()
            self.find_marsha(marsha)  # Beware unregistered click
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