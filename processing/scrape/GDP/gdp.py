import os

import requests
import wget
from bs4 import BeautifulSoup


class GDPScraper:
    """
    The GDPScraper class is used to scrape GDP data from specific URLs.

    Attributes:
        path (str): The local path to save the downloaded files.
        choice (str): The choice of data to scrape ('all', 'merchandise trade', or 'national account').

    Methods: - scrape_gdp_data(path: str, link: str): Scrapes GDP data from the provided link and saves the files
    locally. - scrape_gdp_choice(): Scrapes GDP data based on the user's choice ('all', 'merchandise trade',
    or 'national account').
    """
    def __init__(self, path: str, choice: str):
        self.path = path
        self.choice = choice

    @staticmethod
    def scrape_gdp_data(path: str, link: str):
        """
        Scrapes GDP data from the specified link and saves the files locally.

        Args:
            path (str): The local path to save the downloaded files.
            link (str): The URL containing GDP data to be scraped.
        """

        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html.parser")

        # Specify the destination directory
        destination_dir = os.path.join(path, link.split("/")[-1].replace('statistics-by-', ''))

        # Create the destination directory if it doesn't exist
        os.makedirs(destination_dir, exist_ok=True)

        # Find all <a> tags that have a href attribute containing ".xlsx"
        xlsx = []
        for link in soup.find_all("a", href=True):
            if link["href"].endswith(".xlsx"):
                xlsx.append(link["href"])

        for excel_link in xlsx:
            link = excel_link
            filename = os.path.join(destination_dir)
            wget.download(url=link, out=filename)

    def scrap_GDP_Choice(self):
        """
        Scrapes GDP data based on the user's choice ('all', 'merchandise trade', or 'national account').

        Returns:
            None
        """
        choice = self.choice
        url_select = ["https://gdp.mef.gov.kh/SEAD/statistics-by-merchandise-trade",
                      "https://gdp.mef.gov.kh/SEAD/statistics-by-national-account"]

        if choice == 'All':
            for link in url_select:
                self.scrape_gdp_data(self.path, link)

        elif choice == 'Merchandise trade':
            link = url_select[0]
            self.scrape_gdp_data(self.path, link)
        elif choice == 'National account':
            link = url_select[1]
            self.scrape_gdp_data(self.path, link)
