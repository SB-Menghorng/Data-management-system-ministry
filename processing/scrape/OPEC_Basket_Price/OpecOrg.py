import os

import pandas as pd
import requests
import wget
from bs4 import BeautifulSoup


def opec_org(path):
    """
    Scrapes OPEC data from the specified URL, downloads the files, and saves them locally.

    Args:
        path (str): The local path to save the downloaded files.

    Returns:
        str: Path to the CSV file created from the scraped data.
    """

    # URL of the website to scrape
    # Replace with the URL of the website you want to scrape
    path = os.path.join(path, 'OPEC')
    url = "https://www.opec.org/opec_web/en/data_graphs/40.htm"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    for name in soup.find_all('div', attrs={'class': 'textblock'}):
        for a_link in name.find_all('a', href=True):
            print(a_link['href'])

            # Create the destination directory if it doesn't exist
            os.makedirs(path, exist_ok=True)

            filename = os.path.join(path, a_link['href'].split("/")[-1])
            response = wget.download(url=a_link['href'], out=filename)
            print(' ........... Successfully downloaded!')

    data = pd.read_xml(os.path.join(path, 'basketDayArchives.xml'))
    csv_file = data.to_csv(os.path.join(path, 'OPEC_Basket_Price.csv'))
    data.to_excel(os.path.join(path, 'OPEC_Basket_Price.xlsx'))

    return csv_file

