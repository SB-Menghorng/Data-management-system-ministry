from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from processing.constant import driver_path, user, your_table_name, host, password, database_name
from processing.database import Database
from processing.scrape.Inflation_rate.extract_xml import extract_xml
from processing.scrape.Inflation_rate import calculate

url = 'https://nsdp.gso.gov.vn/index.htm'


class Scraper(webdriver.Chrome):
    """
   The `Scraper` class provides methods for web scraping a specific website using Selenium.

   Attributes:
       driver_path (str): The path to the Chrome WebDriver executable.
       teardown (bool): Whether to quit the WebDriver on exit.

   Methods:
       get_xml(self):
           Scrapes the website to extract XML download links.

       extract_file(self, option, indicator):
           Extracts data from an XML file and processes it based on the selected option and indicator.

       database_connection(self, option=None, indicator=None, create_table=True, table_show=False, delete_table=False, insert_data=False):
           Stores extracted data in a database table with optional table management operations.

   Use Case:
       The `Scraper` class simplifies web scraping tasks using Selenium and facilitates data extraction,
       processing, and database storage.

   Example Usage:
       # Create a Scraper object
       scraper = Scraper(driver_path='chromedriver.exe', teardown=True)

       # Get XML download links from the website
       xml_data = scraper.get_xml()

       # Extract and process data from the XML file
       data_option = 'Consumer Price Index'
       data_indicator = 'PCPICO_PC_PP_PT'
       extracted_data = scraper.extract_file(option=data_option, indicator=data_indicator)

       # Store data in a database table
       scraper.database_connection(option=data_option, indicator=data_indicator, create_table=True)
   """

    def __init__(self, driver=driver_path, teardown=False):
        """
       Initializes a web scraper using Selenium for a specific website.

       Parameters:
       destination_dir (str): The directory where downloaded files will be stored.
       driver (str): The path to the Chrome WebDriver executable.
       teardown (bool): Whether to quit the WebDriver on exit.

       This class extends the webdriver.Chrome class from Selenium to facilitate web scraping.
       It sets up the WebDriver with specific options and provides methods for data extraction.
       """
        self.driver_path = driver
        self.teardown = teardown
        chrome_options = webdriver.ChromeOptions()
        super(Scraper, self).__init__(executable_path=driver, options=chrome_options)
        self.implicitly_wait(2)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Handles the WebDriver cleanup on context exit.

        Parameters:
        exc_type: The type of exception raised (if any).
        exc_val: The exception value.
        exc_tb: The exception traceback.

        If the 'teardown' flag is set to True, this method will quit the WebDriver.
        """
        if self.teardown:
            self.quit()

    def get_xml(self):
        """
       Scrapes the website to extract XML download links.

       Returns:
       dict: A dictionary mapping category names to XML download URLs.

       This method navigates the website and extracts XML download links from a table.
       It returns a dictionary containing category names as keys and download URLs as values.
       """
        self.get(url)
        div = self.find_element(By.ID, "macro-fin-data")
        table = div.find_element(By.TAG_NAME, 'table')
        rows = table.find_elements(By.TAG_NAME, 'tr')

        categories, url_xmls = [], []

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')

            # Check if there are at least 3 cells in the row
            if len(cells) >= 3:
                category_name = cells[0].text
                url_cell = cells[2]

                # Check if there is an <a> element in the cell
                try:
                    url_xml = url_cell.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    print('name:', category_name)
                    print('url:', url_xml)  # Get the href attribute of the <a> element

                    categories.append(category_name)
                    url_xmls.append(url_xml)

                except NoSuchElementException:
                    print('No <a> element found in this cell')
        data_xml = dict(zip(categories, url_xmls))
        print('rows:', len(rows))
        print('data:', data_xml)
        return data_xml

    def extract_file(self, option, indicator):
        """
        Extracts data from an XML file and processes it based on the selected option and indicator.

        Parameters:
        option (str): The selected data option.
        indicator (str): The selected data indicator.

        Returns:
        pd.DataFrame: A DataFrame containing the extracted data.

        This method downloads and extracts data from the selected XML file based on the chosen option and indicator.
        It processes the data and returns a DataFrame.
        """
        data_xml = self.get_xml()
        options = ['National Accounts (GDP)', 'Consumer Price Index', 'General Government Operations',
                   'Central Government Gross Debt', 'Interest Rates', 'Stock Market', 'Balance of Payments',
                   'External Debt', 'Merchandise Trade', 'Exchange Rates']
        if option == options[1]:
            df = extract_xml(data_xml[option])

            if indicator == 'PCPI_IX':
                inflation_rate = calculate.inflation_rate(df)
                df['INFLATION_RATE'] = df['TIME_PERIOD'].map(inflation_rate)
                return df[df['INDICATOR'] == indicator]
            elif indicator == 'PCPICO_PC_PP_PT':
                df1 = df[df['INDICATOR'] == 'PCPICO_PC_PP_PT'].copy()
                df1.rename(columns={'OBS_VALUE': 'Inflation Rate'}, inplace=True)
                df1['Status'] = ['Real'] * df1.shape[0]
                df1['Month'] = df1['TIME_PERIOD'].dt.month
                df1['Year'] = df1['TIME_PERIOD'].dt.year
                months = {1: 'January',
                          2: 'February',
                          3: 'March',
                          4: 'April',
                          5: 'May',
                          6: 'June',
                          7: 'July',
                          8: 'August',
                          9: 'September',
                          10: 'October',
                          11: 'November',
                          12: 'December'}
                df1['Month'] = df1['Month'].map(months)
                df1['Value'] = df1['Inflation Rate']
                df1['Note'] = df[df['INDICATOR'] == 'PCPI_IX']['BASE_PER'].iloc[:df1.shape[0]].values
                df1.rename(columns={'PublishDate': 'Publish Date'}, inplace=True)
                return df1[['Country', 'Source', 'Update frequency', 'Status', 'Year', 'Month', 'Value', 'Publish Date',
                            'Link', 'Note']]
        else:
            print("The option haven't develop yet")

    def database_connection(self, option=None, indicator=None, create_table=True,
                            table_show=False, delete_table=False, insert_data=False):
        """
       Stores extracted data in a database table.

       Parameters:
       option (str): The selected data option.
       indicator (str): The selected data indicator.
       create_table (bool): Whether to create a new table in the database.
       delete_table (bool): Whether to delete the existing table in the database.

       Returns:
       bool: True if the data was successfully inserted into the database, False otherwise.

       This method stores the extracted data in a database table with optional table management operations.
       It returns True if the data insertion is successful, or False if there was an issue.
       """
        if option is None:
            option = 'Consumer Price Index'
        if indicator is None:
            indicator = 'PCPICO_PC_PP_PT'
        db = Database(host, password, user, table=your_table_name, database=database_name)

        if create_table:
            db.create_table()
        elif table_show:
            db.show_table()
        elif delete_table:
            db.delete_table()
        elif insert_data:
            df = self.extract_file(option, indicator)
            db.insert_data(df)


# Example usage:
def main(option=None, indicator=None, create_table=True,
         table_show=False, delete_table=False, insert_data=False):

    if option is None:
        option = 'Consumer Price Index'
    if indicator is None:
        indicator = 'PCPICO_PC_PP_PT'

    scraper = Scraper(teardown=True)
    df = scraper.extract_file(option=option, indicator=indicator)
    # scraper.database_connection(option, indicator, create_table,
    #                             table_show, delete_table, insert_data)
    return df
