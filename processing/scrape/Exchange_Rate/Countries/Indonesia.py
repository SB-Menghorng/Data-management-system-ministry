import os
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from processing.scrape import waiting
from processing.scrape.operations.selenium_ import WebDriverHandler


class ExchangeRate(WebDriverHandler):
    """
    A web scraper class for extracting foreign exchange rate data from the Bank of Indonesia website.

    Inherits from WebDriverHandler for web automation using Selenium.

    Attributes:
        path (str): The directory path where the scraped data will be saved.
        day (int): The day for the data extraction (e.g., 28).
        month (int): The month for the data extraction (e.g., 9).
        year (int): The year for the data extraction (e.g., 2023).

    Methods:
        scrape_exchange_rate_indonesia(self):
            Scrapes foreign exchange rate data from the Bank of Indonesia website for the specified date and currency.
            The scraped data is saved to an Excel file in the provided path.

        Returns:
            str: Path to the saved Excel file.

    Use Case:
        This class simplifies web scraping tasks for foreign exchange rate data using Selenium and provides
        a structured Excel file for further analysis and processing.

    Example Usage:
        # Initialize the ExchangeRate class
        scraper = ExchangeRate(path="/path/to/save/data", day=28, month=9, year=2023)

        # Scrape and save the data to an Excel file
        excel_file_path = scraper.scrape_exchange_rate_indonesia()

        print(f"Data saved to: {excel_file_path}")
    """
    def __init__(self, path, day, month, year):
        super().__init__()
        self.path = path
        self.day = day
        self.month = month
        self.year = year

    def scrape_exchange_rate_indonesia(self):
        """
        Scrapes foreign exchange rate data from the Bank of Indonesia website for the specified date and currency.
        The scraped data is saved to an Excel file in the provided path.

        Returns:
            str: Path to the saved Excel file.
        """

        ################################## Start: Selenium Processes ##################################
        # URL of the page
        url = "https://www.bi.go.id/en/statistik/informasi-kurs/transaksi-bi/Default.aspx"

        # Date you want to select
        year = self.year
        month = self.month
        day = self.day
        target_date = f"{day}-{month}-{year}"

        # Convert the custom date format to the MySQL format 'YYYY-MM-DD'
        date_obj = datetime.strptime(target_date, "%d-%m-%Y")
        date_value = date_obj.strftime("%Y-%m-%d")

        # Set USD Currency as Default
        target_currency = "USD"

        print(f"\nSelected Date: {date_value}")
        print(f"Currency Selected: {target_currency}\n")

        # Open the URL
        self.get(url)

        ################################## Setting Up the Date of Exchange Rate Table
        # Find and interact with the date input field
        date_input = self.find_element(By.ID,
                                         "ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_txtTanggal")
        date_input.send_keys(target_date)
        button = self.find_element(By.ID,
                                     "ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_btnSearch2")

        ################################## Setting Up Currencies
        # Find and interact with the currency dropdown
        currency_dropdown = WebDriverWait(self, 10).until(
            EC.presence_of_element_located(
                (By.ID, "ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_ddlmatauang1"))
        )
        currency_dropdown.send_keys(target_currency)
        # currency_dropdown.send_keys(Keys.ENTER)
        button.click()

        ################################## Start: Waiting ##################################
        waiting()
        ################################## End: Waiting ##################################

        ################################## Start Pulling Data ##################################
        columns = []
        currency_type = []
        value = []
        sell = []
        buy = []
        date = []

        for tr in range(1, 27):
            # Find all <tr>, <td> & <th> elements within the <tbody> using XPath
            table_row_elements = self.find_element(
                By.XPATH,
                f'//*[@id="ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_gvSearchResult2"]')

            if tr == 1:
                th_elements_1 = table_row_elements.find_element(By.XPATH,
                                                                f'//*[@id="ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_gvSearchResult2"]/tbody/tr[1]/th[1]')
                th_elements_2 = table_row_elements.find_element(By.XPATH,
                                                                f'//*[@id="ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_gvSearchResult2"]/tbody/tr[1]/th[2]')
                th_elements_3 = table_row_elements.find_element(By.XPATH,
                                                                f'//*[@id="ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_gvSearchResult2"]/tbody/tr[1]/th[3]')
                th_elements_4 = table_row_elements.find_element(By.XPATH,
                                                                f'//*[@id="ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_gvSearchResult2"]/tbody/tr[2]/td[4]')
                columns.append(th_elements_1.text)
                columns.append(th_elements_2.text)
                columns.append(th_elements_3.text)
                columns.append(th_elements_4.text)
            if tr > 1:
                td_elements_1 = table_row_elements.find_element(
                    By.XPATH,
                    f'//*[@id="ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_gvSearchResult2"]/tbody/tr[{tr}]/td[1]'

                )
                td_elements_2 = table_row_elements.find_element(
                    By.XPATH,
                    f'//*[@id="ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_gvSearchResult2"]/tbody/tr[{tr}]/td[2]')
                td_elements_3 = table_row_elements.find_element(
                    By.XPATH,
                    f'//*[@id="ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_gvSearchResult2"]/tbody/tr[{tr}]/td[3]')
                td_elements_4 = table_row_elements.find_element(
                    By.XPATH,
                    f'//*[@id="ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_gvSearchResult2"]/tbody/tr[{tr}]/td[4]')

                currency_type.append(td_elements_1.text)
                value.append(td_elements_2.text)
                sell.append(td_elements_3.text.replace(',', ''))
                buy.append(td_elements_4.text.replace(',', ''))
                date.append(date_value)
            ################################## End of Pulling Data ##################################

            ################################### Start: DataFrame and Save DataFrame ###################################
            # DataFrame
        df = pd.DataFrame(data={"Date": date,
                                "Currencies": currency_type,
                                "Value": value,
                                "Sell": sell,
                                "Buy": buy},
                          columns=columns)
        print(df)

        """
            - Save DataFrame as .xlsx
            - Specify the destination directory
            - Change this to your desired directory
            - Create the destination directory if it doesn't exist
        """
        os.makedirs(self.path, exist_ok=True)
        filename = f"Exchange_Rate_Indonesia_{date_value}.xlsx"

        # Specify the path for the files
        xlsx_file_path = self.path + '\\' + filename

        df.to_excel(xlsx_file_path, index=False)

        # Check if the CSV and XLSX files exist
        if os.path.exists(xlsx_file_path):
            print(f"\nXLSX files already downloaded and stored at: {xlsx_file_path}")
        else:
            print("\nXLSX files do not exist!")


