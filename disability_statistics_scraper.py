# Script for scraping employment data off disabilitystatistics.org

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import Select
from csv import writer

#Initialize Selenium webdriver for chrome
options = ChromeOptions()
options.add_argument("--incognito")
driver = Chrome(executable_path='c:/Local/chromedriver.exe',port=9515, chrome_options=options)

#Open site to scrape
driver.get('https://disabilitystatistics.org/reports/acs.cfm?statistic=2')

#Initialize site's query tool
content = driver.find_element_by_class_name('stats').find_elements_by_tag_name('tr')
Select(content[1].find_element_by_id('age')).select_by_index(3)
total_years = len(content[1].find_element_by_id('year').find_elements_by_xpath('.//*'))

#Generate Data for each year
for i in xrange(0,total_years):

    Select(content[1].find_element_by_id('year')).select_by_index(i)
    content[1].find_element_by_name('submitButton').click()

    #Refresh content references and retrieve resulting table
    content = driver.find_element_by_class_name('stats').find_elements_by_tag_name('tr')
    years = content[1].find_element_by_id('year').find_elements_by_xpath('.//*')
    results = content[1].find_element_by_class_name('tableData').find_elements_by_tag_name('tr')

    #retrieve data and store in csv
    with open('data_' + str(years[i].text) + '.csv', 'wb') as csv_file:
        csv_writer = writer(csv_file, delimiter=',')
        for row in results:
            data = []
            cols = row.find_elements_by_xpath('td | th')
            for col in cols:
                cell = col.text.encode('ascii', 'ignore').replace(',','')
                if cell.isdigit():
                    cell = float(cell)
                data.append(cell)
            csv_writer.writerow(data)

#Exit Chrome
driver.quit()