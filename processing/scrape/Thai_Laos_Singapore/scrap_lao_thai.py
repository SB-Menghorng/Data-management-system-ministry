from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pandas as pd
from translate import Translator
import requests
from bs4 import BeautifulSoup as bs
import re
import numpy as np
from datetime import datetime
from processing.constant import driver_path

class Webscrape:
    def __init__(self, driver_path):
        self.driver_path = driver_path

    def Browser(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        service = Service(executable_path=self.driver_path)
        browser = webdriver.Chrome(service=service, options=options)
        browser.get(url)
        return browser

    def Thai_Price_Consomer(self):
        url = 'http://www.indexpr.moc.go.th/price_present/cpi/stat/others/report_core1.asp?tb=cpig_index_country&code=93&c_index=a.change_year'
        browser = self.Browser(url)
        wait = WebDriverWait(browser, 20)
        table = wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/table[3]')))
        rows = table.find_elements(By.TAG_NAME, value="tr")
        translator = Translator(from_lang='th', to_lang='en')
        data = []
        for row in rows[3:]:
            cells = row.find_elements(By.TAG_NAME, value="td")
            if len(cells) > 23:
                Now = datetime.now().strftime('%d/%m/%y')
                source = 'Ministry of Commerce of Thailand'
                status = 'Real'
                f_update = 'Monthly'
                country = 'Thailand'
                Pub_Date = np.nan
                Link = url

                datas = [cell.text for cell in cells]

                data.append(datas)

        data = pd.DataFrame(data)
        df = data.iloc[:, :23].copy()
        df.iloc[:, 0] = [translator.translate(month) for month in df.iloc[:, 0]]
        df.iloc[0, :] = [translator.translate(month) for month in df.iloc[0, :]]
        df1 = df.iloc[0, :]
        df1 = np.insert(df1, 0, 'Month')
        df1 = df1[:-1].tolist()
        df.drop(index=df.index[0], axis=0, inplace=True)
        df.columns = df1

        melted_df = pd.melt(df, id_vars='Month', var_name='Year', value_name='Values')
        melted_df['Values'] = melted_df['Values'].replace(' ', np.nan)
        melted_df['Values'] = melted_df['Values'].astype(float)
        melted_df = melted_df.dropna()
        melted_df = melted_df[['Year', 'Month', 'Values']]
        No = melted_df.index
        title = 'Inflation Rate'
        country = 'Thailand'
        source = 'Bank of Thailand'
        f_update = 'Monthly'
        status = 'Real'
        access_daate = datetime.now().strftime('%d/%m/%y')
        pub_date = np.nan
        link = url
        note = 'Rate of change compared to the same month last year'
        melted_df.insert(0, 'No', No)
        melted_df.insert(1, 'Title', title)
        melted_df.insert(2, 'Country', country)
        melted_df.insert(3, 'Source', source)
        melted_df.insert(4, 'Frequency Update', f_update)
        melted_df.insert(5, 'Status', status)
        melted_df.insert(9, 'Access_Date', access_daate)
        melted_df.insert(10, 'Pub_Date', pub_date)
        melted_df.insert(11, 'Link', link)
        melted_df.insert(12, 'Note', note)
        return melted_df[['Month', 'Year']]

    # Scrape Singapore inflation data
    def SG_Inflation(self):
        global link
        url = 'https://www.mas.gov.sg/statistics/mas-core-inflation-and-notes-to-selected-cpi-categories'
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
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

    # Scrape Laos inflation data
    def LaoInflation(self,year):
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
            # col_cells = 
            # Pub_Date = np.nan
            Now = datetime.now().strftime('%d/%m/%y')
            source = ' BANK OF THE LAO P.D.R'
            status = 'Real'
            f_update = 'Monthly'
            country = 'Lao'
            url = 'https://www.bol.gov.la/en/inflation'

            # Extract and store the cell text in a list
            status = 'Real'
            row_data = [year]+[cell.text for cell in cells]+[np.nan]+[Now]+[source]+[status]+[f_update]+[country,url]

            # Append the row data to the data list
            data.append(row_data)
        
        # Define column names
        column_names = ['Year','Note', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'C.Y.Ave.', 'Publish Date','Access Date','Source','Status','Frequency Update','country','Link']  # Repeat for other months and columns

        # Create a DataFrame
        data2 = pd.DataFrame(data, columns=column_names)
        melted_df2 = pd.melt(data2, id_vars=['Year','Note','Publish Date','Access Date','Source','Status','Frequency Update','country','Link'],var_name='Month', value_name='Values')
        melted_df2=melted_df2[~(melted_df2['Note'] !='Inflation Rate (%)')]
        melted_df2['Title'] = melted_df2['Note'].str.replace(r'\s*\(.*\)', '', regex=True)
        melted_df2['Note'] = melted_df2['Note'].replace('Inflation Rate (%)','Just show only month')
        melted_df2=melted_df2[[ 'Title','country', 'Source','Frequency Update', 'Status','Year', 'Month', 'Values', 'Access Date', 'Publish Date',
                'Link','Note']]
        No = melted_df2.index
        melted_df2.insert(0,'No',No)
        melted_df2['Values'] = melted_df2['Values'].replace(r',','.',regex=True).astype(float)
        return melted_df2

def main():
    web = Webscrape(driver_path=driver_path).Thai_Price_Consomer()
    print(web)


if __name__ == '__main__':
    main()