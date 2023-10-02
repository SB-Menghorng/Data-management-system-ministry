import os

import requests
import wget
from bs4 import BeautifulSoup


class NBCDataScraper:
    """
    The NBCDataScraper class is used to scrape financial data from the National Bank of Cambodia (NBC) website.

    Attributes:
        path (str): The local path to save the downloaded files.
        choice (str): The choice of data to scrape ('Monetary and financial statistics data', 'Balance of payment data',
            'Banks reports', 'mfis reports', 'flcs reports', or 'All').

    Methods:
        - scrape_nbc_data(path: str, link: str, choice: str): Scrapes financial data from the specified link and saves
            the files locally.
        - scrape_nbc_choice(): Scrapes financial data based on the user's choice.
    """

    def __init__(self, path: str, choice: str):
        self.path = path
        self.choice = choice

    @staticmethod
    def scrape_nbc_data(path: str, link: str, choice: str):
        """
        Scrapes financial data from the specified link and saves the files locally.

        Args:
            path (str): The local path to save the downloaded files.
            link (str): The URL containing financial data to be scraped.
            choice (str): The choice of data to scrape.

        Returns:
            None
        """
        path = os.path.join(path, 'NBC')
        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html.parser")

        # Specify the destination directory
        destination_dir = os.path.join(path, choice)  # Change this to your desired directory

        # Create the destination directory if it doesn't exist
        os.makedirs(destination_dir, exist_ok=True)

        # Find all <a> tags that have a href attribute containing ".xlsx"
        xlsx_links = []
        for link in soup.find_all("a", href=True):
            if link["href"].endswith(".xlsx"):
                xlsx_links.append(link["href"])

        # Print the links to .xlsx file
        for xlsx_link in xlsx_links:
            url = "https://www.nbc.gov.kh" + xlsx_link[5:]
            print(url)

        for xlsx_link in xlsx_links:
            url = "https://www.nbc.gov.kh" + xlsx_link[5:]
            filename = os.path.join(destination_dir, xlsx_link.split("/")[-1])
            wget.download(url=url, out=filename)

    def scrap_NBC_Choice(self):
        """
        Scrapes financial data based on the user's choice ('Monetary and financial statistics data', 'Balance of payment data',
        'Banks reports', 'mfis reports', 'flcs reports', or 'All').

        Returns:
            None
        """
        choice = self.choice
        path = self.path
        scrap_NBC = self.scrape_nbc_data
        last_words = ['monetary_and_financial_statistics_data',
                      'balance_of_payment_data',
                      'banks_reports',
                      'mfis_reports',
                      'flcs_reports'
                      ]
        url_web = "https://www.nbc.gov.kh/english/economic_research/"
        if choice == 'Monetary and financial statistics data':
            url = url_web + last_words[0] + ".php"
            scrap_NBC(path, url, choice)
        elif choice == 'Balance of payment data':
            url = url_web + last_words[1] + ".php"
            scrap_NBC(path, url, choice)
        elif choice == 'Banks reports':
            url = url_web + last_words[2] + ".php"
            scrap_NBC(path, url, choice)
        elif choice == 'Microfinance Institution(MFI) reports':
            url = url_web + last_words[3] + ".php"
            scrap_NBC(path, url, choice)
        elif choice == 'Financial Literacy Centres(FLCs) reports':
            url = url_web + last_words[4] + ".php"
            scrap_NBC(path, url, choice)
        elif choice == 'All':
            for i in last_words:
                url = url_web + i + ".php"
                scrap_NBC(path, url, i)
