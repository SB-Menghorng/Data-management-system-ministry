from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re
import numpy as np
from datetime import datetime
from processing.constant import driver_path, host, password, user, your_table_name, database_name
from processing.database import Database


# Create a class named Webscrap to encapsulate web scraping functionality
def SG_Inflation():
    url = 'https://www.mas.gov.sg/statistics/mas-core-inflation-and-notes-to-selected-cpi-categories'
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      r'Chrome/117.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = bs(response.content, 'html.parser')
    class_link = soup.find_all('a', class_='mas-link')

    for i in class_link[1:]:
        link = f"https://www.mas.gov.sg{i.get('href')}"
        print(link)

    response1 = requests.get(link, headers=headers)
    # Check if the request was successful (status code 200)
    if response1.status_code == 200:
        # Get the suggested filename from the Content-Disposition header, if present
        content_disposition = response.headers.get('Content-Disposition')

        if content_disposition:
            # Use regular expressions to extract the filename from the header
            filename_match = re.search(r'filename="(.+)"', content_disposition)
            if filename_match:
                suggested_filename = filename_match.group(1)
            else:
                # If the filename cannot be extracted, use a default name
                suggested_filename = 'downloaded_file.xlsx'
        else:
            # If the Content-Disposition header is not present, use a default name
            suggested_filename = 'downloaded_file.xlsx'

        # Open a file and write the binary content of the response to it
        with open(suggested_filename, 'wb') as f:
            f.write(response.content)

        print(f"Downloaded file: {suggested_filename}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


class Webscrap:
    ## The implamentation how to use all function of code below:
    # -----------------------------------------------------------
    """# Create an instance of the Webscrap class
    webscraper = Webscrap(driver_path='path_to_chromedriver')

    # Scrape Thai Price Consumer data and print a summary
    thai_price_consumer_data = webscraper.Thai_Price_Consomer()
    print("Summary of Thai Price Consumer Data:")


    # Scrape Singapore inflation data and print a summary
    print("\nSummary of Singapore Inflation Data:")
    webscraper.SG_Inflation()

    # Scrape Laos inflation data for a specific year (e.g., 2021) and print a summary
    laos_inflation_data = webscraper.LaoInflation(year=2021)
    print("\nSummary of Laos Inflation Data for 2021:")
    """

    # ------------------------------------------------------------------
    def __init__(self, driver_path):
        # self.url = url
        self.driver_path = driver_path
        # self.year = year

    # Initialize a web browser
    def Browser(self, url):
        # Configure Chrome WebDriver in headless mode (optional)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Enable headless mode
        # service = Service(executable_path=self.driver_path)
        browser = webdriver.Chrome(executable_path=self.driver_path, options=options)
        browser.get(url)
        return browser

    # Scrape Thai price consumer data from a webpage
    def Thai_Price_Consomer(self):
        url = 'http://www.indexpr.moc.go.th/price_present/cpi/stat/others/report_core1.asp?tb=cpig_index_country&code=93&c_index=a.change_year'
        browser = self.Browser(url)
        wait = WebDriverWait(browser, 20)
        table = wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/table[3]')))
        rows = table.find_elements(By.TAG_NAME, value="tr")

        data = []
        for row in rows[4:]:
            cells = row.find_elements(By.TAG_NAME, value="td")
            if len(cells) >= 45:
                # Extract data from table cells
                month = cells[0].text
                Now = datetime.now().strftime('%d/%m/%y')
                source = 'Ministry of Commerce'
                status = 'Real'
                f_update = 'Monthly'
                country = 'Thailand'
                GCPI_2002 = cells[1].text
                GCPI_2003 = cells[2].text
                GCPI_2004 = cells[3].text
                GCPI_2005 = cells[4].text
                GCPI_2006 = cells[5].text
                GCPI_2007 = cells[6].text
                GCPI_2008 = cells[7].text
                GCPI_2009 = cells[8].text
                GCPI_2010 = cells[9].text
                GCPI_2011 = cells[10].text
                GCPI_2012 = cells[11].text
                GCPI_2013 = cells[12].text
                GCPI_2014 = cells[13].text
                GCPI_2015 = cells[14].text
                GCPI_2016 = cells[15].text
                GCPI_2017 = cells[16].text
                GCPI_2018 = cells[17].text
                GCPI_2019 = cells[18].text
                GCPI_2020 = cells[19].text
                GCPI_2021 = cells[20].text
                GCPI_2022 = cells[21].text
                GCPI_2023 = cells[22].text
                BCPI_2002 = cells[23].text
                BCPI_2003 = cells[24].text
                BCPI_2004 = cells[25].text
                BCPI_2005 = cells[26].text
                BCPI_2006 = cells[27].text
                BCPI_2007 = cells[28].text
                BCPI_2008 = cells[29].text
                BCPI_2009 = cells[30].text
                BCPI_2010 = cells[31].text
                BCPI_2011 = cells[32].text
                BCPI_2012 = cells[33].text
                BCPI_2013 = cells[34].text
                BCPI_2014 = cells[35].text
                BCPI_2015 = cells[36].text
                BCPI_2016 = cells[37].text
                BCPI_2017 = cells[38].text
                BCPI_2018 = cells[39].text
                BCPI_2019 = cells[40].text
                BCPI_2020 = cells[41].text
                BCPI_2021 = cells[42].text
                BCPI_2022 = cells[43].text
                BCPI_2023 = cells[44].text
                Pub_Date = np.nan
                Link = url
                # Append data to the list
                data.append([month, Now, source, status, f_update, country, GCPI_2002, GCPI_2003, GCPI_2004, GCPI_2005,
                             GCPI_2006, GCPI_2007, GCPI_2008, GCPI_2009,
                             GCPI_2010, GCPI_2011, GCPI_2012, GCPI_2013, GCPI_2014, GCPI_2015, GCPI_2016, GCPI_2017,
                             GCPI_2018, GCPI_2019, GCPI_2020, GCPI_2021, GCPI_2022, GCPI_2023,
                             BCPI_2002, BCPI_2003, BCPI_2004, BCPI_2005, BCPI_2006, BCPI_2007, BCPI_2008, BCPI_2009,
                             BCPI_2010, BCPI_2011, BCPI_2012,
                             BCPI_2013, BCPI_2014, BCPI_2015, BCPI_2016, BCPI_2017, BCPI_2018, BCPI_2019, BCPI_2020,
                             BCPI_2021, BCPI_2022, BCPI_2023, Pub_Date, Link])

        # Map numeric month values to month names
        e = ['January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November', 'December']

        # Create a DataFrame
        column_names = ['Month', 'Access Date', 'Source', 'Status', 'Update frequency', 'Country', 'GCPI_2002',
                        'GCPI_2003', 'GCPI_2004', 'GCPI_2005', 'GCPI_2006', 'GCPI_2007', 'GCPI_2008', 'GCPI_2009',
                        'GCPI_2010', 'GCPI_2011', 'GCPI_2012', 'GCPI_2013', 'GCPI_2014', 'GCPI_2015', 'GCPI_2016',
                        'GCPI_2017', 'GCPI_2018', 'GCPI_2019', 'GCPI_2020', 'GCPI_2021', 'GCPI_2022', 'GCPI_2023',
                        'BCPI_2002', 'BCPI_2003', 'BCPI_2004', 'BCPI_2005', 'BCPI_2006', 'BCPI_2007', 'BCPI_2008',
                        'BCPI_2009', 'BCPI_2010', 'BCPI_2011', 'BCPI_2012',
                        'BCPI_2013', 'BCPI_2014', 'BCPI_2015', 'BCPI_2016', 'BCPI_2017', 'BCPI_2018', 'BCPI_2019',
                        'BCPI_2020', 'BCPI_2021', 'BCPI_2022', 'BCPI_2023', 'Publish Date',
                        'Link']  # Repeat for other columns
        df = pd.DataFrame(data, columns=column_names)

        # Map numeric month values to month names
        dic = dict(zip(df['Month'].to_list(), e))
        df['Month'] = df['Month'].map(dic)
        melted_df = pd.melt(df, id_vars=['Month', 'Access Date', 'Source', 'Status', 'Update frequency', 'Country',
                                         'Publish Date', 'Link'], var_name='Year of GB', value_name='Value')
        melted_df[['Note', 'Year']] = melted_df['Year of GB'].str.split('_', expand=True)
        melted_df.drop(columns=['Year of GB'], inplace=True)
        # Create a dictionary to map 'GCPI' to 'Headline Consumer Price Index' and 'BCPI' to 'Core Consumer Price Index'
        note_mapping = {'GCPI': 'Headline Consumer Price Index', 'BCPI': 'Core Consumer Price Index'}

        # Use the mapping dictionary to update the 'Note' column
        melted_df['Note'] = melted_df['Note'].map(note_mapping)
        # melted_df['Values'] = melted_df['Values'].replace(' ',np.nan)
        return melted_df

    # Scrape Singapore inflation data

    # Scrape Laos inflation data
    def LaoInflation(self, year):
        url = 'https://www.bol.gov.la/en/inflation'
        browser = self.Browser(url)
        select_year = browser.find_element(By.XPATH, '//*[@id="year"]')
        # year = input("Input Year :")
        select_year.send_keys(str(year))
        search_bt = browser.find_element(By.XPATH, '//*[@id="frm_sel"]/div/div[2]/div/button[1]')
        search_bt.click()

        wait = WebDriverWait(browser, 10)
        table = wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="frm_sel"]/div/div[3]/table')))
        # Create an empty list to store the table data
        data = []

        # Find all rows in the table body
        rows = table.find_elements(By.XPATH, './/tbody/tr')

        # Iterate through the rows
        for row in rows:
            # Find all cells in the current row
            cells = row.find_elements(By.XPATH, './/td')
            # Pub_Date = np.nan
            Now = datetime.now().strftime('%d/%m/%y')
            source = ' BANK OF THE LAO P.D.R'
            status = 'Real'
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
                        'Source',
                        'Status', 'Update frequency', 'Country', 'Link']  # Repeat for other months and columns

        # Create a DataFrame
        data2 = pd.DataFrame(data, columns=column_names)
        melted_df2 = pd.melt(data2,
                             id_vars=['Month', 'Access Date', 'Source', 'Status', 'Update frequency',
                                      'Country', 'Publish Date', 'Link', 'Value', 'Note', 'Year'], var_name='Month',
                             value_name='Value')

        browser.quit()
        return melted_df2


def main():
    db = Database(host, password, user, table=your_table_name, database=database_name)
    db.create_table()

    webscraper = Webscrap(driver_path=driver_path)

    # Scrape Thai Price Consumer data and print a summary
    thai_price_consumer_data = webscraper.Thai_Price_Consomer()
    thai_price_consumer_data['Value'] = thai_price_consumer_data['Value'].map(lambda x: float(x))

    print("Summary of Thai Price Consumer Data:", thai_price_consumer_data['Value'])
    db.insert_data(thai_price_consumer_data)

    # Scrape Singapore inflation data and print a summary
    print("\nSummary of Singapore Inflation Data:")
    SG_Inflation()

    # Scrape Laos inflation data for a specific year (e.g., 2021) and print a summary
    laos_inflation_data = webscraper.LaoInflation(year=2021)
    print("\nSummary of Laos Inflation Data for 2021:", laos_inflation_data)
    # db.insert_data(laos_inflation_data)
    db.show_table()


main()
