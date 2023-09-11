from processing.scrape import waiting
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from processing.constant import driver_path
from selenium.webdriver.common.keys import Keys
# import mysql.connector
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import wget
import pandas as pd
import os

from processing.scrape.Banglasdesh_ex_rate.mainb import Banglasdesh
from processing.scrape.Bank_thianland.thailand_exchange_rate import Bank_thailand_scraper
from processing.scrape.E_change_Rate_of_China.my_package.scrapers.forex_scraper import ForexScraper
from processing.scrape.exp_srilanka import exp_sri_lanka
from processing.scrape.ADB import scraper


class Scraper:
    # Initialize variables
    def __init__(self, path, year, month, day):
        self.path = path
        self.year = year
        self.month = month
        self.day = day

    def opec_org(self):
        # URL of the website to scrape
        # Replace with the URL of the website you want to scrape
        url = "https://www.opec.org/opec_web/en/data_graphs/40.htm"
        response = requests.get(url
            # url,
            # verify='/Users/mac/Desktop/PyCharm/lib/python3.11/site-packages/certifi/cacert.pem'
        )
        soup = BeautifulSoup(response.content, "html.parser")
        # print(soup.prettify())

        for name in soup.find_all('div', attrs={'class': 'textblock'}):
            for a_link in name.find_all('a', href=True):
                print(a_link['href'])

                # Specify the destination directory
                # Change this to your desired directory
                # "/Users/mac/Desktop/MoLVT/OPEC Basket Price 2/"
                # destination_dir = self.path

                # Create the destination directory if it doesn't exist
                os.makedirs(self.path, exist_ok=True)

                filename = os.path.join(self.path, a_link['href'].split("/")[-1])
                response = wget.download(url=a_link['href'], out=filename)
                print(' ........... Successfully downloaded!')

        data = pd.read_xml(self.path+ '\\' + 'basketDayArchives.xml')
        csv_file = data.to_csv(self.path +'\\'+ 'OPEC_Basket_Price.csv')
        xlsx_file = data.to_excel(self.path + '\\'+'OPEC_Basket_Price.xlsx')

        return csv_file, xlsx_file

    '''
        In this function, there are -- processes such as:
        * Scraping process: Using Selenium
        * Pandas DataFrame: After scraping the data from exchange table, we store those data in `pd.DataFrame()`
        * Convert dataframe to CSV or XLSX: Still using pandas library `df.to_csv()` or `df.to_xlsx()`
        * Download excel file and store at the specific destionation directory as we desired.
        * MySQL Database: Since the data in form of table and we can desire it as structure data, so we decided to store 
        all the data in MySQL Database.
    '''

    def ExchangeRateIndonesia(self):
        """
        :param path: Set your own laptop or desktop destination directory to store files or data.
            Example: /Users/mac/Desktop/MoLVT/Indonesia Exchange Rate/
            ** Note: ** Directory Path changes based on your OS (Window, Mac, Linux, ...)
        :param year: year of exchange rate table.
        :param month: month of exchange rate table.
        :param day: day of exchange rate table.

        :returns
            1. DataFrame
            2. Convert from dataframe to excel file (*.xlsx)
            3. Store table data to MySQL Database
                ** Note: ** If you want to store data to MySQL Database, you may have to set the configuartion on some points
                such as
                    'host': '...',
                    'user': '...',
                    'password': '...',
                    'database': '...'
                to be able to store data to your database.
            4. Excel file store in your `desired directory` you set earlier and has the name as your `filename` you set
            earlier as well.

        *** Hope you understand! Have a nice day! :) ***
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

        os.environ['PATH'] += driver_path

        # Create a webdriver instance using the Service object
        driver = webdriver.Chrome(executable_path=driver_path)

        # Open the URL
        driver.get(url)

        ################################## Setting Up the Date of Exchange Rate Table
        # Find and interact with the date input field
        date_input = driver.find_element(By.ID,
                                         "ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_txtTanggal")
        date_input.send_keys(target_date)
        button = driver.find_element(By.ID, "ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_btnSearch2")


        ################################## Setting Up Currencies
        # Find and interact with the currency dropdown
        currency_dropdown = WebDriverWait(driver, 10).until(
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
            table_row_elements = driver.find_element(
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

        to_xlsx = df.to_excel(xlsx_file_path, index=False)

        # Check files if they are existed!

        # Check if the CSV and XLSX files exist
        if os.path.exists(xlsx_file_path):
            print(f"\nXLSX files already downloaded and stored at: {xlsx_file_path}")
        else:
            print("\nXLSX files do not exist!")
        ################################### End: DataFrame and Save DataFrame ###################################

        # Close the browser window
        driver.quit()
        # ################################## End of Selenium Process ##################################
        #
        # ################################## Start Storing in Database Process ##################################
        # db_config = {
        #     'host': '127.0.0.1',
        #     'user': 'root',
        #     'password': 'LaySENG./333',
        #     'database': 'MoLVT'
        # }
        # conn = mysql.connector.connect(**db_config)
        # cursor = conn.cursor()
        #
        # # Create a table
        # create_table_query = '''
        #         CREATE TABLE IF NOT EXISTS indonesia_exchange_rate (
        #             id INT AUTO_INCREMENT PRIMARY KEY,
        #             date DATE,
        #             currencies VARCHAR(5),
        #             value FLOAT,
        #             sell FLOAT,
        #             buy FLOAT
        #         )
        #     '''
        # cursor.execute(create_table_query)
        #
        # # Check if the data already exists
        # query_for_checking = 'SELECT date FROM indonesia_exchange_rate WHERE date = %s'
        # cursor.execute(query_for_checking, (date_value,))
        # checking_results = cursor.fetchall()
        #
        # # Check if there are any results
        # if checking_results:
        #     # The data already exists
        #     # Stop the execution
        #     print("\nPlease Try Again! It seems some issues happened!")
        #     raise Exception('The data already exists.')
        # else:
        #     # Insert data into the table
        #     for i in range(len(currency_type)):
        #         insert_query = '''
        #                 INSERT INTO indonesia_exchange_rate (date, currencies, value, sell, buy) VALUES (%s, %s, %s, %s, %s)
        #             '''
        #         exchange_data = (date_value, currency_type[i], value[i], sell[i], buy[i])
        #         cursor.execute(insert_query, exchange_data)
        #
        #     # Commit changes
        #     conn.commit()
        #
        # # Write a SQL query to select the data
        # query = f'SELECT * FROM indonesia_exchange_rate;'
        # cursor.execute(query)
        # results = cursor.fetchall()
        #
        # # Check if the results are empty
        # if not results:
        #     print('\nThe data is not stored in the database.')
        # else:
        #     print('\nThe data is also stored in the database.')
        #
        # # Close the cursor and connection
        # cursor.close()
        # conn.close()
        ################################## End of Storing in Database Process ##################################

        # return value for further use
        return to_xlsx

    def thailand_exchange_rate(self):
        path = self.path
        scraping = Bank_thailand_scraper(path)
        scraping.land_first_page()
        scraping.get_csv()

    def exp_srilanka(self):
        path = self.path
        exp_sri_lanka(path)

    def adb(self):
        path = self.path
        scraper(path)

    def china_exchange_rate(self, path, start_date, end_date, driver_path=driver_path):
        # Specify the target currency
        target_currency = "USD"
        driver_path = driver_path

        # Initialize the ForexScraper with the provided driver_path
        scraper = ForexScraper(driver_path)

        # Scrape forex data
        forex_data = scraper.scrape_data(target_currency, start_date, end_date)

        # Specify the destination directory for the CSV file
        destination_dir = path  # Use the provided path as the destination directory

        # Create the destination directory if it doesn't exist
        os.makedirs(destination_dir, exist_ok=True)

        # Define the CSV file name based on start_date and end_date
        csv_filename = f"chExRate_{start_date}_to_{end_date}.csv"

        # Construct the full path to the CSV file
        csv_filepath = os.path.join(destination_dir, csv_filename)

        # Save the scraped data to the CSV file
        forex_data.to_csv(csv_filepath, index=False)

        print(f"Data saved to {csv_filepath}")

    def banglashdesh_ex_rate(self, input_date_str):
        path = self.path
        scraping = Banglasdesh(path)
        scraping.mainbd(path,input_date_str,driver_path=driver_path)






