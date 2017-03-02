from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import Select
from csv import writer
from os import path
from os import makedirs

#Function to store tables as csv files
def to_csv(results, disability_status, year):
    with open('data/data_' + disability_status + '_' + year + '.csv', 'wb') as csv_file:
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

#---------------------------------------------------------------------------------------------------------------------#

#Initialize Selenium webdriver for chrome
options = ChromeOptions()
options.add_argument("--incognito")
driver = Chrome(executable_path='c:/Local/chromedriver.exe',port=9515, chrome_options=options)

#Open site to scrape
driver.get('https://disabilitystatistics.org/reports/acs.cfm?statistic=2')

#Create directory for csv files
if not path.exists('data'):
    makedirs('data')

#Initialize site's query tool
content = driver.find_element_by_class_name('stats').find_elements_by_tag_name('tr')
Select(content[1].find_element_by_id('age')).select_by_index(3)
total_years = len(content[1].find_element_by_id('year').find_elements_by_xpath('.//*'))

#Generate Data for each year
for i in xrange(0,total_years):
    for j in xrange(1,3):

        Select(content[1].find_element_by_id('year')).select_by_index(i)
        Select(content[1].find_element_by_id('disabilityStatus')).select_by_index(j)
        content[1].find_element_by_name('submitButton').click()

        #Refresh content references and retrieve resulting table
        content = driver.find_element_by_class_name('stats').find_elements_by_tag_name('tr')
        disability_status = content[1].find_element_by_id('disabilityStatus').find_elements_by_xpath('.//*')[j].text
        year = content[1].find_element_by_id('year').find_elements_by_xpath('.//*')[i].text
        results = content[1].find_element_by_class_name('tableData').find_elements_by_tag_name('tr')

        #store table in csv
        to_csv(results,disability_status,year)

#Exit Chrome
driver.quit()