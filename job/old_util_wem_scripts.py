
colorama.init(autoreset=True)

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


def add_category():
    # marsha = 'TAEMR'
    # marsha_location['page'] = 1
    # marsha_location['nth-child'] = 3

    xpath_to_tbody = '//div[@class="x-panel-body x-grid-body' + \
        ' x-panel-body-default-framed x-panel-body-default-framed x-layout-fit"]' + \
        '[contains(@id, "vui-vcm-ui-picker-")]//div//table//tbody'
    # Wait for folders to load
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, xpath_to_tbody+'//tr[position()=2]') ))
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
    # end of if block
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
        # Close categories to prepare for add_category_from_results, or return to page 1
        return False
