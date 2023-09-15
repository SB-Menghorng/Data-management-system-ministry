from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import pandas as pd
# import pymysql
# import mysql.connector
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import time

def waiting2():
    max_timeout = 5
    remaining_time = max_timeout

    while remaining_time > 0:
        print(f"Waiting... {remaining_time} seconds remaining")
        time.sleep(1)
        remaining_time -= 1

def inflation_indonesia():
    # URL of the page
    url = "https://www.bi.go.id/en/statistik/indikator/data-inflasi.aspx"

    # Driver Path
    driver_path = "/Users/mac/Documents/chromedriver-mac-x64/chromedriver"

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless mode

    # Create a Service object
    service = Service(driver_path)

    # Create a webdriver instance using the Service object
    driver = webdriver.Chrome(service=service)

    # Open the URL
    driver.get(url)

    columns = []                # Use to keep headers
    date = []                   # Use to keep date
    inflation_data = []         # Use to keep inflation rate data

    '''
        Because of it has <thead> and inside <thead> has <tr> which contains columns name. 
        So, I need to specify it first.   
    '''
    th_elements_1 = driver.find_element(By.XPATH,
                                        f'//*[@id="tableData"]/table/thead/tr/th[1]')
    th_elements_2 = driver.find_element(By.XPATH,
                                        f'//*[@id="tableData"]/table/thead/tr/th[2]')
    columns.append(th_elements_1.text)
    columns.append(th_elements_2.text)

    for page in range(1, 26):
        if page >= 1 and page <= 24:
            for tr in range(1, 11):   # Set fixed amount of <tr> in each page
                '''
                      In this section, I start pulling data from <tbody> which contains 10 <tr> tags as well.
                '''
                td_elements_1 = driver.find_element(
                    By.XPATH,
                    f'/html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div/div[2]/div[1]/div/div[1]/div[4]/table/tbody/tr[{tr}]/td[1]')
                td_elements_2 = driver.find_element(
                    By.XPATH,
                    f'/html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div/div[2]/div[1]/div/div[1]/div[4]/table/tbody/tr[{tr}]/td[2]')

                date.append(td_elements_1.text)
                inflation_data.append(td_elements_2.text)

            print(f"Page {page} is done!")

            next_button = driver.find_element(
                By.CLASS_NAME, f'next')
            next_button.send_keys(Keys.ENTER)
            waiting2()

        if page == 25:
            for tr in range(1, 10):  # Set fixed amount of <tr> in each page
                '''
                      In this section, I start pulling data from <tbody> which contains 10 <tr> tags as well.
                '''
                td_elements_1 = driver.find_element(
                    By.XPATH,
                    f'/html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div/div[2]/div[1]/div/div[1]/div[4]/table/tbody/tr[{tr}]/td[1]')
                td_elements_2 = driver.find_element(
                    By.XPATH,
                    f'/html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div/div[2]/div[1]/div/div[1]/div[4]/table/tbody/tr[{tr}]/td[2]')

                date.append(td_elements_1.text)
                inflation_data.append(td_elements_2.text)

            print(f"Page 25 is done!")
            print(f"Data is fully scraped!")

    # DataFrame
    df = pd.DataFrame(data={"Date": date,
                            "Inflation Data": inflation_data},
                      columns=columns)

    path = "/Users/mac/Desktop/MoLVT/Indo Inflation"
    df.to_csv(path + "/IndoInflation.csv", index=False)

    print("\n")
    print(df)

    driver.quit()

inflation_indonesia()