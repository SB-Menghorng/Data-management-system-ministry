from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from processing.constant import driver_path, user, your_table_name, host, password, database_name
from processing.database import Database
from processing.scrape.Inflation_rate.extract_xml import extract_xml
from processing.scrape.Inflation_rate import calculate

url = 'https://nsdp.gso.gov.vn/index.htm'


class Scraper(webdriver.Chrome):
    def __init__(self, destination_dir, driver=driver_path, teardown=False):
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
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": destination_dir
        })
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
                return df1
        else:
            print("The option haven't develop yet")

    def store_database(self, option='Consumer Price Index', indicator='PCPICO_PC_PP_PT', create_table=True,
                       delete_table=False):
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
        db = Database(host, password, user, table=your_table_name, database=database_name)

        df = self.extract_file(option, indicator)
        if create_table:
            db.create_table(your_table_name)
        elif delete_table:
            db.delete_table()

        db.insert_data(df, InflationRate='Inflation Rate', TimePeriod='TIME_PERIOD', Country='Vietnam',
                       Status='Observation', PublishDate='2023-08-29',
                       links='https://nsdp.gso.gov.vn/index.htm',
                       note_value='2019')


# Example usage:
# dir_store = r"D:\Intership\Labour ministry of combodain\demo"
# scraper = Scraper(destination_dir=dir_store, teardown=True)
# df = scraper.extract_file('Consumer Price Index', 'PCPICO_PC_PP_PT')
# scraper.store_database('Consumer Price Index', 'PCPICO_PC_PP_PT', create_table=True, delete_table=False)
# print(df)
