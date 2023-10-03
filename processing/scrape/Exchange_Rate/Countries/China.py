import os

import pandas as pd
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from processing.scrape.operations.selenium_ import WebDriverHandler


class ForexScraper(WebDriverHandler):
    """
    ForexRateScraper is a web scraper class for extracting foreign exchange rate data from the Bank of China website.

    Inherits from WebDriverHandler for web automation.

    Attributes:
        None

    Methods:
        scrape_exchange_rates(self, target_currency, start_date, end_date):
            Scrapes foreign exchange rate data for a given target currency and date range from the website.

        Parameters:
            target_currency (str): The target currency code to scrape data for (e.g., 'USD').
            start_date (str): The start date for the data extraction in the format 'YYYY-MM-DD'.
            end_date (str): The end date for the data extraction in the format 'YYYY-MM-DD'.

        Returns:
            pandas.DataFrame: A DataFrame containing the scraped exchange rate data.

    Use Case:
        This class simplifies web scraping tasks for foreign exchange rate data using Selenium and provides
        a structured DataFrame for further analysis and processing.
    """

    def __init__(self, target_currency, start_date, end_date_, path):
        self.target_currency = target_currency
        self.start_date = start_date
        self.end_date = end_date_
        self.path = os.path.join(path, 'China')
        os.makedirs(self.path, exist_ok=True)
        super().__init__()

    def scrape_data(self):
        """
        Scrapes foreign exchange rate data from the Bank of China website.

        Args:
            target_currency (str): The target currency code to scrape data for (e.g., 'USD').
            start_date (str): The start date for the data extraction in the format 'YYYY-MM-DD'.
            end_date (str): The end date for the data extraction in the format 'YYYY-MM-DD'.

        Returns:
            pandas.DataFrame: A DataFrame containing the scraped exchange rate data.
        """
        target_currency = self.target_currency
        start_date = self.start_date
        end_date = self.end_date
        url = 'https://www.boc.cn/sourcedb/whpj/enindex2.htm'
        self.get(url)
        iframe_element = self.find_element(By.XPATH, '//*[@id="DataList"]')
        self.switch_to.frame(iframe_element)

        button_start = self.find_element(By.XPATH, '//*[@id="historysearchform"]/input[1]')
        button_end = self.find_element(By.XPATH, '//*[@id="historysearchform"]/input[2]')
        wait = WebDriverWait(self, 10)
        select_button = wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="historysearchform"]/select')))
        # select_button = self.browser.find_element(By.XPATH, '//*[@id="historysearchform"]/select')
        select_button.send_keys(target_currency)
        button_start.send_keys(start_date)
        button_end.send_keys(end_date)

        search_button = self.find_element(By.XPATH, '//*[@id="historysearchform"]/input[3]')
        search_button.click()

        data = []
        # for n in range(num_pages):
        #     print("Scrapped page", n + 1)
        # Get the total number of pages from the page information
        page_info = wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="list_navigator"]/span[1]')))
        total_pages = int(page_info.find_element(By.CLASS_NAME, 'nav_pagenum').text)
        # Handle the error here, e.g., by waiting and retrying or exiting gracefully.
        print("Number of Total pages in this interval are # ", total_pages)
        # print("Number of Total pages in this interval ",total_pages)
        for n in range(total_pages):
            # print("Scrapped page", n + 1)
            # n=n+1
            wait = WebDriverWait(self, 10)
            try:
                # Wait for the table to be present
                table = wait.until(ec.presence_of_element_located((By.XPATH, "/html/body/table[2]")))

                rows = table.find_elements(By.TAG_NAME, value="tr")
                for i, row in enumerate(rows):
                    if i == 0:
                        continue
                    cells = row.find_elements(By.TAG_NAME, value="td")
                    if len(cells) >= 7:
                        currency_name = cells[0].text
                        buying_rate = cells[1].text
                        cash_buying_rate = cells[2].text
                        selling_rate = cells[3].text
                        cash_selling_rate = cells[4].text
                        middle_rate = cells[5].text
                        pub_time = cells[6].text

                        data.append([currency_name, buying_rate, cash_buying_rate, selling_rate,
                                     cash_selling_rate, middle_rate, pub_time])
                        print(
                            f"Currency: {currency_name}, Buying Rate: {buying_rate}, Cash_buying_rate :{cash_buying_rate},"
                            f"Selling Rate: {selling_rate}, Cahs_selling_rate : {cash_selling_rate}, Middle_rate : {middle_rate},"
                            f"Pub Time: {pub_time}")
                        # pub_time_date = datetime.strptime(pub_time, "%Y.%m.%d %H:%M:%S").strftime("%y-%m-%d")
                        # if pub_time_date < start_date:
                        # break
                try:
                    button_next = wait.until(
                        ec.element_to_be_clickable((By.XPATH, '//*[@id="list_navigator"]/span[3]/a')))
                    button_next.click()
                except (TimeoutException, NoSuchElementException):
                    print("No 'Next' button found or it's not clickable.")
                    break  # Exit the loop if 'Next' button is not found

            except TimeoutException:
                print("Timeout occurred while waiting for elements to load.")
                break  # Exit the loop if timeout occurs

        columns = ["Currency Name", "Buying Rate", "Cash Buying Rate", "Selling Rate", "Cash Selling Rate",
                   "Middle Rate", "Pub Time"]
        df = pd.DataFrame(data, columns=columns)
        return df

    def save_china_exchange_rate_data(self):
        """
        Scrapes foreign exchange rate data from the Bank of China website for the specified date range and target currency.
        The scraped data is saved to a CSV file in the provided path.

        Returns:
            str: Path to the saved CSV file.
        """
        start_date = self.start_date
        end_date = self.end_date
        path = self.path

        # Scrape forex data
        forex_data = self.scrape_data()

        # Specify the destination directory for the CSV file
        destination_dir = path  # Use the provided path as the destination directory

        # Create the destination directory if it doesn't exist
        os.makedirs(destination_dir, exist_ok=True)

        # Define the CSV file name based on start_date and end_date
        csv_filename = f"China_{start_date}_to_{end_date}.csv"

        # Construct the full path to the CSV file
        csv_filepath = os.path.join(destination_dir, csv_filename)

        # Save the scraped data to the CSV file
        forex_data.to_csv(csv_filepath, index=False)

        print(f"Data saved to {csv_filepath}")
