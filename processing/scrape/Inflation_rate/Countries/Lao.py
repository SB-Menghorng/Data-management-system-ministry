from datetime import datetime

import numpy as np
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from processing.connection.database import Database
from processing.constant import host, password, user, table_name1, database_name
from processing.scrape.operations.selenium_ import WebDriverHandler


class LaoInflationDataScraper:
    """
    The LaoInflationDataScraper class is used to scrape and process inflation rate data for Laos.

    Attributes:
        None

    Methods:
        - scrape_inflation_data(year): Scrapes and processes inflation rate data for the specified year.
    """
    def __init__(self, driver):
        self.driver = driver

    def scrape_inflation_data(self, year):
        """
        Scrapes and processes inflation rate data for the specified year.

        Args:
            year (int): The year for which to fetch data.

        Returns:
            pandas.DataFrame: A DataFrame containing processed inflation rate data for Laos.
        """
        url = 'https://www.bol.gov.la/en/inflation'
        self.driver.get(url)
        select_year = self.driver.find_element(By.XPATH, '//*[@id="year"]')
        # year = input("Input Year :")
        select_year.send_keys(str(year))
        search_bt = self.driver.find_element(By.XPATH, '//*[@id="frm_sel"]/div/div[2]/div/button[1]')
        search_bt.click()

        wait = WebDriverWait(self.driver, 10)
        table = wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="frm_sel"]/div/div[3]/table')))
        # Create an empty list to store the table data
        data = []

        # Find all rows in the table body
        rows = table.find_elements(By.XPATH, './/tbody/tr')

        # Iterate through the rows
        for row in rows:
            # Find all cells in the current row
            cells = row.find_elements(By.XPATH, './/td')
            # col_cells =
            # Pub_Date = np.nan
            Now = datetime.now().strftime('%d/%m/%y')
            source = ' BANK OF THE LAO P.D.R'
            'Real'
            f_update = 'Monthly'
            country = 'Lao'
            url = 'https://www.bol.gov.la/en/inflation'

            # Extract and store the cell text in a list
            status = 'Real'
            row_data = [year] + [cell.text for cell in cells] + [np.nan] + [Now] + [source] + [status] + [f_update] + [
                country, url]

            # Append the row data to the data list
            data.append(row_data)

        # Define column names
        column_names = ['Year', 'Note', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                        'September', 'October', 'November', 'December', 'C.Y.Ave.', 'Publish Date', 'Access Date',
                        'Source', 'Status', 'Update frequency', 'Country',
                        'Link']  # Repeat for other months and columns

        # Create a DataFrame
        data2 = pd.DataFrame(data, columns=column_names)
        melted_df2 = pd.melt(data2, id_vars=['Year', 'Note', 'Publish Date', 'Access Date', 'Source', 'Status',
                                             'Update frequency', 'Country', 'Link'], var_name='Month',
                             value_name='Value')
        melted_df2 = melted_df2[~(melted_df2['Note'] != 'Inflation Rate (%)')]
        melted_df2['Title'] = melted_df2['Note'].str.replace(r'\s*\(.*\)', '', regex=True)
        melted_df2['Note'] = melted_df2['Note'].replace('Inflation Rate (%)', 'Just show only month')
        melted_df2 = melted_df2[
            ['Title', 'Country', 'Source', 'Update frequency', 'Status', 'Year', 'Month', 'Value', 'Access Date',
             'Publish Date',
             'Link', 'Note']]
        No = melted_df2.index
        melted_df2.insert(0, 'No', No)
        melted_df2['Value'] = melted_df2['Value'].replace(r',', '.', regex=True).astype(float)
        return melted_df2


# db = Database(host, password, user, table=your_table_name, database=database_name)
# wb = LaoInflationDataScraper(WebDriverHandler())
# db.insert_data(wb.scrape_inflation_data(2020))

