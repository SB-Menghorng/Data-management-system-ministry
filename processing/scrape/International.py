from processing.scrape.Inflation_rate import InflationScraper
import os.path

from processing.scrape.OPEC_Basket_Price import OpecOrg
from processing.scrape.Exchange_Rate.ExchangeRateScraper import ExchangeRate

from processing.scrape.Export import ExportScraper


class Scraper:
    def __init__(self, choice, destinationDir, day, start_date, end_date, month, year, month_year,
                 currency='USD'):
        self.choice = choice
        self.start_date = start_date
        self.end_date = end_date
        self.currency = currency
        self.day = day
        self.month = month
        self.year = year
        self.month_year = month_year
        self.destinationDir = os.path.join(destinationDir, "International")

    def ExchangeRate(self):
        scraper = ExchangeRate(day=self.day, destination_path=self.destinationDir, currency=self.currency,
                               option=self.choice, start_date=self.start_date,
                               end_date=self.end_date, month=self.month, year=self.year, month_year=self.month_year)
        scraper.scrape()

    def Export(self):
        scraper = ExportScraper.Export(self.destinationDir)
        scraper.srilanka()

    def OpecBasketPrice(self):
        OpecOrg.opec_org(self.destinationDir)

    def InflationRate(self):
        InflationScraper.InflationRate(self.year, option=self.choice)
