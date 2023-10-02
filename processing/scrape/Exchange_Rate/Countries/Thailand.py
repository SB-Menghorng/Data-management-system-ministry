from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from processing.scrape.operations.selenium_ import WebDriverHandler


class BankThailandScraper(WebDriverHandler):
    """
       A web scraper class for extracting exchange rate data from the Bank of Thailand website.

       Inherits from WebDriverHandler for web automation.

       Attributes:
           None

       Methods:
           navigate_to_first_page(self):
               Navigate to the first page of the Bank of Thailand website.

           download_exchange_rate_csv(self):
               Download exchange rate data in CSV format from the website.
               This function clicks necessary buttons to trigger the download of exchange rate data.

       Use Case:
           This class simplifies web scraping tasks for exchange rate data from the Bank of Thailand using Selenium.
       """

    def download_exchange_rate_csv(self):
        """
        Download exchange rate data in CSV format from the website.

        This function clicks necessary buttons to trigger the download of exchange rate data.
        """
        self.get("https://www.bot.or.th/en/statistics/exchange-rate.html")
        wait = WebDriverWait(self, 10)  # 10 seconds maximum wait time

        # Wait for the "Got It" button to be clickable
        got_it_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="container-55222efc2a"]/div/div['
                                                                         '3]/div/div/div/div/table/tbody/tr['
                                                                         '3]/td[3]/button/span')))
        got_it_button.click()
        if got_it_button:
            print('get to first step', got_it_button)

        # Click the currency element
        currency_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="container-b9454cb2b1"]/div/div['
                                                                            '2]/bot-statistics/div['
                                                                            '2]/div/div/div/div/div/div/div['
                                                                            '2]/div/div[2]/div['
                                                                            '2]/div/button[2]/i')))
        currency_element.click()
        if currency_element:
            print('get into currency', currency_element)

        # Click the download CSV button
        download_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="container-b9454cb2b1"]/div/div['
                                                                           '2]/bot-statistics/div['
                                                                           '2]/div/div/div/div/div/div/div['
                                                                           '2]/div/div[2]/div[2]/div/div[2]/ul/li['
                                                                           '1]/button')))

        download_button.click()
        if download_button:
            print('download button clicked..', download_button)
