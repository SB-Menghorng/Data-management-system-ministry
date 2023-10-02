import os.path

from processing.scrape.GDP.gdp import GDPScraper
from processing.scrape.NBC import nbc


class Scraper:
    def __init__(self, destination_dir, choice):
        self.destinationDir = os.path.join(destination_dir, 'DomesticData')
        self.choice = choice

    def ExchangeRate(self):
        pass

    def Export(self):
        pass

    def GDP(self):
        scraper = GDPScraper(os.path.join(self.destinationDir, 'GDP'), self.choice)
        scraper.scrap_GDP_Choice()

    def NBC(self):
        scraper = nbc.NBCDataScraper(self.destinationDir, self.choice)
        scraper.scrap_NBC_Choice()
