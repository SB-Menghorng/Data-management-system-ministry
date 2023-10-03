import os.path
from datetime import datetime

import pandas as pd
from selenium.webdriver.common.by import By
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

    def __init__(self, destinationDir):

        super().__init__()
        self.storeDir = os.path.join(destinationDir, 'Thailand')
        os.makedirs(self.storeDir, exist_ok=True)

    def download_exchange_rate_csv(self):
        """
        Download exchange rate data in CSV format from the website.

        This function clicks necessary buttons to trigger the download of exchange rate data.
        """
        self.get("https://www.bot.or.th/en/statistics/exchange-rate.html")
        cookies = self.get_cookies()
        print(cookies)
        print(len(cookies))
        # Loop through the cookies list and add each cookie to the WebDriver instance
        for cookie in cookies:
            self.add_cookie(cookie)

        self.get("https://www.bot.or.th/en/statistics/exchange-rate.html")

        table = self.find_element(By.ID, "table_tab_1")
        print('Table', table)

        header = table.find_element(By.CLASS_NAME, "table-header")
        print('header', header)
        table_header = header.find_element(By.TAG_NAME, 'table')
        print('table header', table_header)
        thead = table_header.find_element(By.TAG_NAME, 'thead').text
        print('Thead', thead)

        table_body = table_header.find_element(By.TAG_NAME, 'tbody')
        print('Body', table_body)
        rows_currency = table_body.find_elements(By.TAG_NAME, 'tr')
        currency = []
        for row in rows_currency:
            currency.append(row.text.replace('\n', ' '))

        print(currency)
        content = table.find_element(By.CLASS_NAME, "table-content")
        print('content', content)

        table_content = content.find_element(By.TAG_NAME, 'table')
        thead_table_content = table_content.find_element(By.TAG_NAME, 'thead')
        rows_thead = thead_table_content.find_elements(By.TAG_NAME, 'tr')

        columns = []
        for row in rows_thead:
            cells = row.find_elements(By.TAG_NAME, 'th')
            for cell in cells:
                columns.append(cell.text)

        print('columns', columns)

        body_content = content.find_element(By.TAG_NAME, 'tbody')
        rows_content = body_content.find_elements(By.TAG_NAME, 'tr')
        columns = columns[2:4] + [columns[1]]
        print(columns)
        datas = [columns]
        for row in rows_content:
            data = []
            cells = row.find_elements(By.TAG_NAME, 'td')
            for cell in cells:
                data.append(cell.text)
            datas.append(data)

        print(datas)
        df = pd.DataFrame(datas[1:], columns=datas[0])
        df[thead] = currency
        columns_show = [df.columns.tolist()[-1]] + df.columns.tolist()[:-1]
        df1 = df[columns_show]
        print(df1)
        # Get the current date and time
        current_time = datetime.now()

        # Format the timestamp as a string without invalid characters
        formatted_time = current_time.strftime('%Y-%m-%d')
        df1.to_csv(os.path.join(self.storeDir, f'{formatted_time}.csv'), index=False)


