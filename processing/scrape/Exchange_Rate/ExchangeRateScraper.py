import os
from processing.scrape.Exchange_Rate.Countries import ADB, Bangladesh, China, Indonesia, Thailand


class ExchangeRate:
    """
    The `ExchangeRate` class provides methods for scraping exchange rate data from various countries' official sources.

    Attributes:
        destinationPath (str): The destination directory for storing the scraped data.

    Methods:
        __init__(self, destination_path, currency, option, start_date, end_date, month, year):
            Initializes the ExchangeRate class with the specified parameters.

        scrape(self):
            Scrapes exchange rate data based on the specified options and parameters.
    """

    def __init__(self, destination_path, option, day, start_date, end_date, month, year, month_year, currency='USD'):
        self.day = day
        self.start_date = start_date
        self.end_date = end_date
        self.month = month
        self.year = year
        self.month_year = month_year
        self.option = option
        self.currency = currency
        self.destinationPath = os.path.join(destination_path, 'ExchangeRate')

    def scrape(self):
        if self.option == 'All':
            self.ADB()
            self.Bangladesh()
            self.China()
            self.Indonesia()
            self.Thailand()
        elif self.option == 'ADB':
            self.ADB()
        elif self.option == 'Bangladesh':
            self.Bangladesh()
        elif self.option == 'China':
            self.China()
        elif self.option == 'Indonesia':
            self.Indonesia()
        elif self.option == 'Thailand':
            self.Thailand()

    def ADB(self):
        ADB.adb_data_scraper(self.destinationPath)

    def Bangladesh(self):
        Bangladesh.ExchangeRateScraperBB().scrape_exchange_rate(destination_dir=self.destinationPath,
                                                                input_date_str=self.month_year,
                                                                target_currency=self.currency)

    def China(self):
        scraper = China.ForexScraper(path=self.destinationPath, start_date=self.start_date, end_date_=self.end_date,
                                     target_currency=self.currency)
        scraper.save_china_exchange_rate_data()

    def Indonesia(self):
        scraper = Indonesia.ExchangeRate(path=self.destinationPath, day=self.day, month=self.month,
                                         year=self.year)
        scraper.scrape_exchange_rate_indonesia()

    def Thailand(self):
        scraper = Thailand.BankThailandScraper(destinationDir=self.destinationPath)
        scraper.download_exchange_rate_csv()
