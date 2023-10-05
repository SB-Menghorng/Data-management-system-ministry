from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from processing.scrape.Inflation_rate.Operations.extract_xml import extract_xml
from processing.scrape.operations.selenium_ import WebDriverHandler


class InflationRateScraper:
    """
    The JapanInflationDataScraper class is used to scrape and process inflation rate data for Japan.

    Attributes:
        None

    Methods:
        - fetch_xml_data(): Fetches XML data from a specific website.
        - extract_inflation_data(option=None): Extracts and processes inflation rate data.

    Inherited Attributes (from WebDriverHandler):
        - None
    """

    def __init__(self, driver):
        self.driver = driver

    def get_xml(self):
        """
        Fetches XML data from the e-stat.go.jp website and returns it in a structured format.

        Returns:
            dict: A dictionary containing XML data organized by sectors and data categories.
        """
        self.driver.get('https://www.e-stat.go.jp/en/data/nsdp/')
        table = self.driver.find_element(By.TAG_NAME, "table").find_element(By.TAG_NAME, 'tbody')
        tables = table.find_elements(By.CLASS_NAME, 'success')
        print('Table', len(tables))
        table_name = []
        for table_ in tables:
            table_name.append(table_.text)
        print(table_name)
        rows = table.find_elements(By.TAG_NAME, 'tr')
        print('rows', len(rows))

        xml_url = []
        sector = []
        for row in rows[:15]:
            data_categories = []
            links = []
            cells = row.find_elements(By.TAG_NAME, 'td')

            if len(cells) > 0:
                sector.append(cells[0].text)
            for cell in cells:
                category = cell.text
                print(category)
                try:
                    href = cell.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    print(href)
                except NoSuchElementException:
                    href = 'No <a> element found in this cell'
                    print(href)

                data_categories.append(category)
                links.append(href)
            try:
                xml_url.append(dict(zip(data_categories, links)))
            except Exception as e:
                print('Error occurred', e)

        print(dict(zip(sector, xml_url)))
        return dict(zip(sector, xml_url))

    def extract_data(self, option=None):
        """
        Extracts and processes inflation rate data based on the provided option.

        Args:
            option (str, optional): The data category option to extract (default is 'Consumer Price Index').

        Returns:
            pandas.DataFrame: A DataFrame containing processed inflation rate data.
        """
        dict_ = self.get_xml()

        if option is None:
            option = 'Consumer Price Index'

        if option == 'Consumer Price Index':
            xml = dict_[option]['SDMX-ML']
            df = extract_xml(xml, country_="Japan", source_="E-state", link_="https://www.e-stat.go.jp/en/data/nsdp/")
            df1 = df.copy()
            df1.rename(columns={'OBS_VALUE': 'Value'}, inplace=True)
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
            df1['Note'] = df[df['INDICATOR'] == 'PCPI_IX']['BASE_PER'].iloc[:df1.shape[0]].values
            df1.rename(columns={'PublishDate': 'Publish Date'}, inplace=True)
            return df1[['Country', 'Source', 'Update frequency', 'Status', 'Year', 'Month', 'Value', 'Publish Date',
                        'Link', 'Note']]


