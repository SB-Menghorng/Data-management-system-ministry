import os.path

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from processing.scrape.operations.selenium_ import WebDriverHandler


class ExchangeRateScraperBB(WebDriverHandler):
    """
    A class for scraping exchange rate data from the website of BB (Bangladesh Bank).

    Inherits WebDriverHandler for handling the web driver.
    """

    def scrape_exchange_rate(self, destination_dir, target_currency, input_date_str):
        """
        Scrape the exchange rate data for a specific target currency and input date.

        Args:
            target_currency (str): The target currency code.
            input_date_str (str): The input date in string format.

        Returns:
            pd.DataFrame: A DataFrame containing the scraped exchange rate data.
            :param destination_dir:
            :param year:
            :param target_currency:
            :param month:
        """
        destination_dir = os.path.join(destination_dir, 'Bangladesh')
        os.makedirs(destination_dir, exist_ok=True)
        url = "https://www.bb.org.bd/en/index.php/econdata/exchangerate"
        self.get(url)

        select_button = self.find_element(By.XPATH, value='//select[@id="inputGroupSelect01"]')
        select_button.send_keys(target_currency)

        input_date = self.find_element(By.XPATH, value='//*[@id="dob"]')
        input_date.send_keys(input_date_str)

        wait = WebDriverWait(self, 20)
        search_button = self.find_element(By.XPATH, '//*[@id="search-form"]/div[3]/button')
        self.execute_script("arguments[0].scrollIntoView();", search_button)
        self.execute_script("arguments[0].click();", search_button)

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
        df1 = pd.DataFrame(data, columns=column_names)
        df1.to_csv(os.path.join(destination_dir, f'{input_date_str}.csv'))
        return df1


