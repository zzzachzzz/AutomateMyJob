from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pprint import pprint
import logging
import json
import time
import re
# import colorama


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('tagging_check.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class Job:
    def __init__(self, marsha='MCOSI', instance='01'):
        self.marsha = marsha
        self.instance = instance
        self.marsha_location = { 'nth-child': 0, 'page': 0 }  # Location in WEM folders
        print("Job instance created")
    
    def launch(self):
        self.driver = webdriver.Ie()
        self.driver.implicitly_wait(120)  # Waits 2 minutes before throwing exception
        # self.driver.get('file:///D:/Users/Zach/Desktop/haha/2OpenText%20Web%20Experience%20Management.htm')
        self.driver.get('http://wemprod.marriott.com:27110/content/#/workspace/folder/hotelwebsites/us/r/rutlc/IPP01')

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
        tile = re.search(r'((?<=Tile)|(?<=Type)|(?<=TITLE))[A-Z]', name)
        if tile:
            tile = 'Tile ' + tile.group()
        content = {
            'skittle_backlink': { 'regex': r'_backToParentLink', 'tag': 'textLink' },
            'skittle_meta': { 'regex': r'_meta', 'tag': 'HotelOverview' },
            'skittle_hero': { 'regex': r'_singleHeroImage', 'tag': 'singleHeroImage' },
            'skittle_B': { 'regex': r'_HotelOverview', 'tag': 'HotelOverview' },
            'skittle_C': { 'regex': r'_headingTextListOfArticles', 'tag': tile },
            'skittle_D': { 'regex': r'_imageHeaderTextCtaAdvanced', 'tag': tile },
            'skittle_E': { 'regex': r'_imageHeaderTextCta(?!Advanced)', 'tag': tile },
            'header_C': { 'regex': r'_headingTextListOfArticles_TITLE[A-Z]', 'tag': 'Header' },
            'header_E': { 'regex': r'_imageHeaderTextCta_TITLE[A-Z]', 'tag': 'Header' },
        }
        mi = r'[A-Z]{5}_IPP[0-9]{2}'  # marsha_and_instance
        article = r'_Article[0-9]{1,2}_(Tile|Type)[A-Z]'
        wrapper = r'(?<!_Article[0-9])_(Tile|Type)[A-Z]' # 'Tile A'
        # header_C = { 'regex': r'_headingTextListOfArticles_TITLE[A-Z]', 'tag': 'Header' }  #TITLEA & tag 'Tile A'
        # header_E = { 'regex': r'_imageHeaderTextCta_TITLE[A-Z]', 'tag': 'Header' }  #TITLE & tag 'imageHeaderTextCta'
        
        if re.search(r'^(TRASH|ZZTRASH)', name) or re.search(article, name):
            return []  # No tags expected
        for k, v in content.items():
            # print(k, v)
            if re.search(v['regex'], name):
                if k in {'skittle_backlink', 'skittle_meta', 'skittle_hero', 'skittle_B'}:
                    return [v['tag'], self.marsha, self.instance]
                elif k in {'header_C', 'header_E'}:
                    return [v['tag'], tile, self.marsha, self.instance]
                elif k in {'skittle_C', 'skittle_D', 'skittle_E'}:
                    if re.search(wrapper, name):
                        return [v['tag'], self.marsha, self.instance]
                    elif re.search(article, name):
                        return []
        return "Made it through the loop??? Ok"


    def verify_tags(self, marsha, instance):
        self.marsha = marsha
        self.instance = instance
        # e = self.find_e('#vui-workspace-grid-body > div > table > tbody > tr:nth-child('+str(i)+')')
        tbody = self.find_e('#vui-workspace-grid-body > div > table > tbody')
        tr_child_len = len(tbody.find_elements_by_tag_name('tr'))
        for i in range(2, tr_child_len):
            e = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td:nth-child(3) > div > div')
            name = e.text  # System Name
            e = tbody.find_element_by_css_selector('tr:nth-child('+str(i)+') > td:nth-child(2) > div > ul > li:nth-child(2)')  # Properties button
            print("-------------------------------")
            print(name)
            expected_tags = self.get_expected_tags(name)  # Returns set
            # print(expected_tags)
            e.click()
            # Menu bar "Overview, Translations, Publishing, Channels, Categories, etc"
            e = self.find_e('div.x-tab-bar-body.x-tab-bar-body-top.x-tab-bar-body-default-top.x-tab-bar-body-horizontal.x-tab-bar-body-default-horizontal.x-tab-bar-body-default.x-tab-bar-body-default-top.x-tab-bar-body-default-horizontal.x-tab-bar-body-default-docked-top.x-box-layout-ct')
            ### Click Categories Tab ####
            categories_tab = e.find_element_by_css_selector('div:nth-child(2) > div > div:nth-child(5) > em > button')
            categories_tab.click()
            # wait = WebDriverWait(driver, 5)
            # wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '')))
            time.sleep(3)
            e = self.driver.find_elements_by_xpath('//div[starts-with(@id, "CATEGORY_ASSOCIATIONS_GRID_")]')[1]
            
            # Old
            # actual_tags = e.text.split()
            # New
            actual_tags = [s.strip() for s in e.text.split('\n')]

            ### Iterate through, checking against expected tags ###
            # for tag in categories #
            # S = {'YULSA', '04', 'TileB'}  # Expected
            # L = ['MCOSI', '04', 'TileA']  # Actual
            print("Expected: {}".format(expected_tags))
            print("Actual: {}".format(actual_tags))
            if len(expected_tags) == 0:
                print('No tags expected')
                for tag in actual_tags:
                    print("Tag should not be present: {}".format(tag))
            else:
                for tag in expected_tags:
                    if tag not in actual_tags:
                        print('{} expected, is missing'.format(tag))
                        # logger.info('Expected {}'.format(x))  # Log the missing tag
                    else:
                        print('{} found'.format(tag))
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
                if (re.search(r'^[\s]*[A-Z]{5}[\s]*$', cell.text) or  # If a marsha tag
                    re.search(r'^[\s]*0{1}[0-9]{1}[\s]*$', cell.text)):  # If an instance tag
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


# pprint(dir(e.job))

# Time it
# start_time = time.clock()
# print("{}".format(time.clock() - start_time))

# Target Category Tree 
# '#vui-vcm-ui-picker-1444-category-tree_header-body'
# x-panel-header-body x-panel-header-body-default x-panel-header-body-horizontal x-panel-header-body-default-horizontal x-panel-header-body-top x-panel-header-body-default-top x-panel-header-body-docked-top x-panel-header-body-default-docked-top x-panel-header-body-default-horizontal x-panel-header-body-default-top x-panel-header-body-default-docked-top x-box-layout-ct

# Tree Node Expanded
# x-grid-row x-grid-tree-node-expanded


# e = self.driver.find_elements_by_xpath('//div[@role="presentation"][@class="x-box-inner x-vertical-box-overflow-body"]') # returns list
# e.find_elements_by_tag_name('div')[1].find_element_by_css_selector('div > a')
# Quick Action CONTEXT MENU
# <div id="menu-1205-innerCt" class="x-box-inner x-vertical-box-overflow-body" role="presentation" style="height: 58px; width: 149px;">
#   <div class="x-menu-icon-separator" id="vext-gen1862" style="height: 58px;">&nbsp;</div>
#   <div id="menu-1205-targetEl" style="position:absolute;width:20000px;left:0px;top:0px;height:1px">
#     <div id="menuitem-1203" class="x-component x-box-item x-component-default x-menu-item" style="left: 0px; top: 0px; margin: 0px;">
#       <a id="menuitem-1203-itemEl" class="x-menu-item-link" href="#" hidefocus="true" unselectable="on">
#         <img id="menuitem-1203-iconEl" src="data:image/gif;base64,R0lGODlhAQABAID/AMDAwAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==" class="x-menu-item-icon vui-drawer-contextmenu-edit">
#         <span id="menuitem-1203-textEl" class="x-menu-item-text">Quick Action Settings...</span>
#         <img id="menuitem-1203-arrowEl" src="data:image/gif;base64,R0lGODlhAQABAID/AMDAwAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==" class="">
#       </a>
#     </div>
#     <div id="menuitem-1204" class="x-component x-box-item x-component-default x-menu-item" style="left: 0px; top: 27px; margin: 0px; width: 149px;">
#       <a id="menuitem-1204-itemEl" class="x-menu-item-link" href="#" hidefocus="true" unselectable="on">
#         <img id="menuitem-1204-iconEl" src="data:image/gif;base64,R0lGODlhAQABAID/AMDAwAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==" class="x-menu-item-icon vui-drawer-contextmenu-delete">
#         <span id="menuitem-1204-textEl" class="x-menu-item-text">Remove Quick Action</span>
#         <img id="menuitem-1204-arrowEl" src="data:image/gif;base64,R0lGODlhAQABAID/AMDAwAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==" class="">
#       </a>
#     </div>
#   </div>
# </div>

# SELECT SIDEBAR FILE NAVIGATION
# Parent
# MARSHA CODES (nth-child) 
# <tr class="x-grid-row x-grid-tree-node-expanded" id="vext-gen3886"><td class="x-grid-cell-treecolumn x-grid-cell x-grid-cell-treecolumn-1716 x-grid-cell-first" id="vext-gen3990"><div class="x-grid-cell-inner " style="text-align: left; ;"><img src="data:image/gif;base64,R0lGODlhAQABAID/AMDAwAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==" class="x-tree-elbow-empty"><img src="data:image/gif;base64,R0lGODlhAQABAID/AMDAwAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==" class="x-tree-elbow-plus x-tree-expander"><img src="data:image/gif;base64,R0lGODlhAQABAID/AMDAwAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==" class="x-tree-icon x-tree-icon-parent vui-tree-category x-tree-icon x-tree-icon-leaf">MARSHA Codes</div></td></tr>
# Upon expanding, folders are inserted into the dom as sibling???
# id 4000+ right after expanded folder

# Example A (marsha codes > A)
# <tr id="vext-gen4095" class="x-grid-row x-grid-row-selected x-grid-row-focused"><td class="x-grid-cell-treecolumn x-grid-cell x-grid-cell-treecolumn-1716   x-grid-cell-first"><div class="x-grid-cell-inner " style="text-align: left; ;"><img src="data:image/gif;base64,R0lGODlhAQABAID/AMDAwAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==" class="x-tree-elbow-empty"><img src="data:image/gif;base64,R0lGODlhAQABAID/AMDAwAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==" class="x-tree-elbow-line"><img src="data:image/gif;base64,R0lGODlhAQABAID/AMDAwAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==" class="x-tree-elbow-plus x-tree-expander"><img src="data:image/gif;base64,R0lGODlhAQABAID/AMDAwAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==" class="x-tree-icon x-tree-icon-parent vui-tree-category x-tree-icon x-tree-icon-leaf">A</div></td></tr>


# Getting Sidebar Category Tree
"""
>>> e = job.driver.find_elements_by_css_selector('div.x-panel-body.x-grid-body.x-panel-body-default.x-panel-body-default.x-layout-fit')
>>> e[2].get_attribute('id')
'vui-vcm-ui-picker-1444-category-tree-body'
>>>
"""

# REFRESH BUTTON
# <div id="button-1028" class="x-btn x-box-item x-toolbar-item x-btn-default-toolbar-small x-icon x-btn-icon x-btn-default-toolbar-small-icon" style="border-width: 1px; left: 213px; top: 0px; margin: 0px;">
#   <em id="button-1028-btnWrap">
#     <button id="button-1028-btnEl" type="button" class="x-btn-center" hidefocus="true" role="button" autocomplete="off" data-qtip="Refresh" style="height: 16px;">
#       <span id="button-1028-btnInnerEl" class="x-btn-inner" style="">&nbsp;</span>
#       <span id="button-1028-btnIconEl" class="x-btn-icon x-tbar-loading"></span>
#     </button>
#   </em>
# </div>

