import pandas as pd
from selenium.webdriver.common.by import By
from translate import Translator

from processing.scrape.Inflation_rate.Countries.Vietnam import Scraper
from processing.scrape.operations.selenium_ import WebDriverHandler


def translate_to_english(text):
    """
    Translates text from Thai to English using the Translator class.

    Args:
        text (str): The text to be translated in Thai.

    Returns:
        str: The translated text in English.
    """
    translator = Translator(from_lang='th', to_lang='en')
    translated_text = translator.translate(text)
    return translated_text


class ThaiConsumerPriceScraper:
    """
    The ThaiConsumerPriceScraper class is used to scrape and process consumer price data for Thailand.

    Attributes:
        None

    Methods:
        - scrape_consumer_price_data(): Scrapes consumer price data from the Bank of Thailand website.
    """
    def __init__(self, driver):
        self.driver = driver

    def scrape_consumer_price_data(self):
        """
        Scrapes consumer price data from the Bank of Thailand website and processes it.

        Returns:
            pandas.DataFrame: A DataFrame containing processed consumer price data for Thailand.
        """
        url = 'http://www.indexpr.moc.go.th/price_present/cpi/stat/others/report_core1.asp?tb=cpig_index_country&code=93&c_index=a.change_year'
        self.driver.get(url)
        tables = self.driver.find_elements(By.TAG_NAME, 'table')
        print('The number of table:', len(tables))

        note = tables[0].find_elements(By.TAG_NAME, 'tr')[0].text[-32:]
        note = translate_to_english(note)
        print(note)
        table = tables[-1]
        rows = table.find_elements(By.TAG_NAME, 'tr')
        print('The number of rows in the last table:', len(rows))

        row_indicator = rows[2].find_elements(By.TAG_NAME, 'td')
        indicators = []
        for indicator in row_indicator:
            indicators.append(indicator.text)
        indicators = [translate_to_english(i) for i in indicators]
        print('Indicator:', indicators)

        # translate_indicators = ['General Consumer Price Index', 'Basic Consumer Price Index']
        # map_indicators = dict(zip(indicators, translate_indicators))
        # print('map:', map_indicators)

        rows_data = []
        row_years = rows[3].find_elements(By.TAG_NAME, 'td')
        years = []
        for cell_ in row_years:
            years.append(int(cell_.text) - 543)
        print(years)
        months = []
        for row in rows[4:]:
            cells = row.find_elements(By.TAG_NAME, 'td')
            print('cells', len(cells))
            row_data = []
            for cell in cells:
                data = cell.text
                row_data.append(data)
            months.append(row_data[0])

            rows_data.append(row_data[1:])

            print('Row scraped:', len(rows_data))
        print(rows_data)
        months = [translate_to_english(x) for x in months]
        # translating_month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
        #                      'October', 'November', 'December']
        # map_month = dict(zip(months, translating_month))
        # print(map_month)

        datas = {'Year': [], 'Month': [], 'Value': [], 'Indicator': [], 'Note': []}

        count_year = 1
        for i, year_ in enumerate(years):
            started_year = years[0]
            if i > 0:
                if year_ == started_year:
                    count_year += 1

            for month_, datas_ in zip(months, rows_data):
                datas['Year'].append(year_)
                datas['Month'].append(month_)
                datas['Value'].append(datas_[i])
                datas['Note'].append(note)

                if count_year >= 2:
                    datas['Indicator'].append(indicators[-1])
                else:
                    datas['Indicator'].append(indicators[0])

        df = pd.DataFrame(datas)
        # df['Indicator'] = df['Indicator'].map(map_indicators)
        # df['Month'] = df['Month'].map(map_month)
        # df['Indicator'] = df['Indicator'].apply(lambda x: translate_to_english(x))
        # df['Month'] = df['Month'].apply(lambda x: translate_to_english(x))
        df['Value'] = df['Value'].apply(lambda x: x.replace(' ', 'NaN'))
        df.dropna(subset=['Value'], inplace=True)
        df['Value'] = df['Value'].astype(float)
        unique_value = lambda x: [x] * df.shape[0]
        df['Country'] = unique_value('Thailand')
        df['Source'] = unique_value('Bank of Thailand')
        df['Status'] = unique_value('Real')
        df['Publish Date'] = unique_value('None')
        df['Update frequency'] = unique_value('Monthly')
        df['Link'] = unique_value(url)
        df = df[df['Indicator'] == indicators[0]]

        print(df)
        return df[['Country', 'Source', 'Update frequency', 'Status', 'Year', 'Month', 'Value', 'Publish Date',
                   'Link', 'Note']]

# ok = ThaiConsumerPriceScraper(WebDriverHandler())
# df = ok.scrape_consumer_price_data()
