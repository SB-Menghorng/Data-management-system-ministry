from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pandas as pd

class ExchangeRateScraperbb:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.service = Service(executable_path=self.driver_path)
        self.browser = webdriver.Chrome(executable_path=self.driver_path)

    def scrape_exchange_rate(self, target_currency, input_date_str):
        url = "https://www.bb.org.bd/en/index.php/econdata/exchangerate"
        self.browser.get(url)

        select_button = self.browser.find_element(By.XPATH, value='//select[@id="inputGroupSelect01"]')
        select_button.send_keys(target_currency)

        input_date = self.browser.find_element(By.XPATH, value='//*[@id="dob"]')
        input_date.send_keys(input_date_str)

        wait = WebDriverWait(self.browser, 20)
        search_button = wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="search-form"]/div[3]/button')))
        self.browser.execute_script("arguments[0].scrollIntoView();", search_button)
        self.browser.execute_script("arguments[0].click();", search_button)

        table = wait.until(ec.presence_of_element_located((By.XPATH, "//table")))

        rows = table.find_elements(By.TAG_NAME, "tr")
        data = []
        for row in rows[2:]:  # Skip the header rows
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 3:
                date = cells[0].text
                usd_buy = cells[1].text
                usd_sell = cells[2].text
                data.append([date, usd_buy, usd_sell])

        # Create a DataFrame
        column_names = ['Date', 'USD Buy', 'USD Sell']
        df = pd.DataFrame(data, columns=column_names)
        return df
