import pandas as pd
import requests

from processing.constant import headers
from processing.scrape.Inflation_rate.calculate import calculate_inflation_rate_general
from processing.scrape.driver import WebDriverHandler
from selenium.webdriver.common.by import By


class InflationRateScraper(WebDriverHandler):
    """
    The InflationRateScraper class is used to scrape and process inflation rate data for Singapore.

    Attributes:
        None

    Methods:
        - fill_missing_years(df): A static method that fills missing 'Year' values in a DataFrame.
        - preprocess_data(df): Modifies the DataFrame containing scraped data.
        - scrape_and_process_data(): Scrapes and returns a list of DataFrames containing inflation rate data.

    Inherited Attributes (from WebDriverHandler):
        - None
    """

    @staticmethod
    def fill_missing_years(df):
        """
        Fills missing 'Year' values in a DataFrame by propagating non-zero values from previous rows.

        Args:
            df (pandas.DataFrame): The input DataFrame with 'Year' column.

        Returns:
            pandas.DataFrame: A modified DataFrame with missing 'Year' values filled.
        """
        df1 = df.copy()
        for i in range(1, df1.shape[0]):
            if df1.loc[i, 'Year'] == 0:
                df1.loc[i, 'Year'] = df1.loc[i - 1, 'Year']
        return df1

    def preprocess_data(self, df):
        """
        Modifies a DataFrame containing scraped data to conform to a specific format.

        Args:
            df (pandas.DataFrame): The input DataFrame with raw scraped data.

        Returns:
            pandas.DataFrame: A modified DataFrame with standardized columns.
        """

        unique_value = lambda x: [x] * df.shape[0]
        df['Month'] = df.iloc[:, 0].apply(lambda x: x.split(' ')[1] if len(x.split(' ')) > 1 else x.split(' ')[0])
        df['Year'] = df.iloc[:, 0].apply(lambda x: x.split(' ')[0] if len(x.split(' ')) > 1 else 0).astype(int)
        df = self.fill_missing_years(df)
        df['Note'] = df.columns[1]
        df['Update frequency'] = unique_value('Monthly')
        df['Country'] = unique_value('Singapore')
        df['Source'] = unique_value('GOV')
        df['Status'] = unique_value('Real')
        df['Indicator'] = unique_value("Inflation")
        df['Publish Date'] = unique_value('None')
        df['Link'] = unique_value(
            'https://www.mas.gov.sg/statistics/mas-core-inflation-and-notes-to-selected-cpi-categories')
        df.drop(columns=df.columns[0], inplace=True)
        df.rename(columns={'Index (Year 2019=100)': 'CPI'}, inplace=True)
        df = calculate_inflation_rate_general(df)
        df = df[
            ['Country', 'Source', 'Update frequency', 'Status', 'Year', 'Month', 'Value', 'Publish Date', 'Link',
             'Note']]
        return df

    def scrape_and_process_data(self):
        """
        Scrapes inflation rate data from a website, processes it, and returns a list of DataFrames.

        Returns:
            List[pandas.DataFrame]: A list of DataFrames containing processed inflation rate data.
        """

        self.get('https://www.mas.gov.sg/statistics/mas-core-inflation-and-notes-to-selected-cpi-categories')
        contain = self.find_element(By.CLASS_NAME, "mas-section")
        as_ = contain.find_elements(By.TAG_NAME, 'a')

        excel_urls = []
        for a in as_:
            excel_urls.append(a.get_attribute('href'))

        dfs = []
        for url in excel_urls:
            response = requests.get(url, headers=headers)
            df = pd.read_excel(response.content, header=1)
            df = self.preprocess_data(df)
            dfs.append(df)

        return dfs


# scraping = InflationRateScraper(teardown=False)
# print(scraping.scrape_and_process_data()[1].info())
