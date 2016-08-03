from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common import action_chains

from time import sleep

buffer_size = 0
output_file = open('dir_list.csv', 'w', buffer_size)
row = 'company_name,country,website,current_url,products'
output_file.write(row + '\n')

wd = webdriver.PhantomJS()

wd.get('http://www.automechanikadubai.com/exhibitor-list.aspx?doc_id=398')
page_number = 0

while page_number < 191:
    wd.implicitly_wait(2)

    try:
        next_button = wd.find_element_by_id('next-span')  # the element you want to scroll to
        action_chains.ActionChains(wd).move_to_element(next_button).perform()
        next_button.click()
    except Exception,e:
        wd.back()
        next_button = wd.find_element_by_id('next-span')  # the element you want to scroll to
        print next_button.get_attribute('url')
        action_chains.ActionChains(wd).move_to_element(next_button).perform()

    page_number += 1

    for _ in range(10):
        result_id = 'ContentPlaceHolder1_rptExhibitor_lnkExhibitorTitle_%d' % _
        cmp_name = ''

        try:
            results = wd.find_element_by_id(result_id)
            cmp_name = results.text.replace(',', ' ')
            results.click()
        except WebDriverException as e:
            continue

        expand_link = wd.find_element_by_link_text('Expand All')

        try:
            content_val = wd.find_element_by_class_name('treeview-red').text.replace('\n', ';')
            content = '[%s]' % content_val
        except WebDriverException as e:
            continue

        country = website = current_url = ''
        try:
            country = wd.find_element_by_css_selector('span.country-list + ul').text.strip()
            website = wd.find_element_by_css_selector('a.web').text
            current_url = wd.current_url
        except WebDriverException as e:
            print 'some content missing'

        row = cmp_name + ',' + country + ',' + website + ',' + current_url + ',' + content
        wd.back()
        output_file.write(row.encode('utf-8') + '\n')
        prev_url = current_url


wd.quit()
