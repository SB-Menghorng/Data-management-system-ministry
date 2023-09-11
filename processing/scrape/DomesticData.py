import os
import wget

import requests
from bs4 import BeautifulSoup


class GDP:
    def __init__(self, path: str, choice: str):
        self.path = path
        self.choice = choice

    def scrap_GDP(self, path: str, link: str):

        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html.parser")

        # Specify the destination directory
        destination_dir = path + '\\' + link.split("/")[-1].replace('statistics-by-', '')

        # Create the destination directory if it doesn't exist
        os.makedirs(destination_dir, exist_ok=True)

        # Find all <a> tags that have an href attribute containing ".xlsx"
        xlsx = []
        for link in soup.find_all("a", href=True):
            if link["href"].endswith(".xlsx"):
                xlsx.append(link["href"])

        for excel_link in xlsx:
            link = excel_link
            filename = os.path.join(destination_dir)
            response = wget.download(url=link, out=filename)

    def scrap_GDP_Choice(self):
        choice = self.choice
        url_select = ["https://gdp.mef.gov.kh/SEAD/statistics-by-merchandise-trade",
                      "https://gdp.mef.gov.kh/SEAD/statistics-by-national-account"]

        if choice == 'all':
            for link in url_select:
                self.scrap_GDP(self.path, link)

        elif choice == 'merchandise trade':
            link = url_select[0]
            self.scrap_GDP(self.path, link)
        elif choice == 'national account':
            link = url_select[1]
            self.scrap_GDP(self.path, link)


class NBC:

    def __init__(self, path: str, choice: str):
        self.path = path
        self.choice = choice

    def scrap_NBC(self, path: str, link: str, choice: str):
        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html.parser")

        # Specify the destination directory
        destination_dir = path + '\\' + choice  # Change this to your desired directory

        # Create the destination directory if it doesn't exist
        os.makedirs(destination_dir, exist_ok=True)

        # Find all <a> tags that have an href attribute containing ".xlsx"
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
            response = wget.download(url=url, out=filename)

    def scrap_NBC_Choice(self):
        choice = self.choice
        path = self.path
        scrap_NBC = self.scrap_NBC
        last_words = ['monetary_and_financial_statistics_data',
                      'balance_of_payment_data',
                      'banks_reports',
                      'mfis_reports',
                      'flcs_reports'
                      ]
        url_web = "https://www.nbc.gov.kh/english/economic_research/"
        if choice == 'monetary_and_financial_statistics_data':
            url = url_web + last_words[0] + ".php"
            scrap_NBC(path, url, choice)
        elif choice == 'balance_of_payment_data':
            url = url_web + last_words[1] + ".php"
            scrap_NBC(path, url, choice)
        elif choice == 'banks_reports':
            url = url_web + last_words[2] + ".php"
            scrap_NBC(path, url, choice)
        elif choice == 'mfis_reports':
            url = url_web + last_words[3] + ".php"
            scrap_NBC(path, url, choice)
        elif choice == 'flcs_reports':
            url = url_web + last_words[4] + ".php"
            scrap_NBC(path, url, choice)
        elif choice == 'all':
            for i in last_words:
                url = url_web + i + ".php"
                scrap_NBC(path, url, i)

