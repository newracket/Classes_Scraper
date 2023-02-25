import pandas as pd
# from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

CAPEURL = 'https://cape.ucsd.edu/responses/Results.aspx'
CAPEDUMPURL = 'https://cape.ucsd.edu/responses/Results.aspx?Name=%2C'
CAPETITLE = 'Course And Professor Evaluations (CAPE)'

def getData():
    # launch browser using Selenium, need to have Firefox installed
    print('Opening a browser window...')
    # driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=Service("./chromedriver.exe"))
    print('Browser window open, loading the page...')

    # get the page that lists all the data, first try
    driver.get(CAPEURL)
    print('Please enter credentials...')

    # wait until SSO credentials are entered
    wait = WebDriverWait(driver, 60)
    element = wait.until(expected_conditions.title_contains(CAPETITLE))

    # get the page that lists all the data
    # (%2C is the comma, drops all the data since every professor name has it)
    driver.get(CAPEDUMPURL)

    # read in the dataset from the html file
    df = pd.read_html(driver.page_source)[0]
    print('Dataset parsed, closing browser window.')

    # destroy driver instance
    driver.quit()

    return df

data = getData()
f = open("data.txt", 'w')
f.write(data)
f.close()