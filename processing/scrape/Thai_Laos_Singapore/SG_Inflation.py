import urllib.request
from bs4 import BeautifulSoup as bs
import wget
import requests
import re

# Create a class named Webscrape to encapsulate web scraping functionality
def SG_Inflation():
    global link
    url = 'https://www.mas.gov.sg/statistics/mas-core-inflation-and-notes-to-selected-cpi-categories'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36'
    }

    # Create a request with headers
    request = urllib.request.Request(url=url, headers=headers)

    try:
        # Open the URL and read its content
        response = urllib.request.urlopen(request)
        content = response.read()

        soup = bs(content, 'html.parser')
        class_link = soup.find_all('a', class_='mas-link')

        for i in class_link[1:]:
            link = f"https://www.mas.gov.sg{i.get('href')}"

        print(link)

        filename = link.split("/")[-1]
        wget.download(link, out=filename)

        response1 = requests.get(link, headers=headers)
        # Check if the request was successful (status code 200)
        if response1.status_code == 200:
            # Get the suggested filename from the Content-Disposition header, if present
            content_disposition = response.headers.get('Content-Disposition')
            if content_disposition:
                # Use regular expressions to extract the filename from the header
                filename_match = re.search('filename="(.+)"', content_disposition)
                if filename_match:
                    suggested_filename = filename_match.group(1)
                else:
                    # If the filename cannot be extracted, use a default name
                    suggested_filename = 'downloaded_file.xlsx'
            else:
                # If the Content-Disposition header is not present, use a default name
                suggested_filename = 'downloaded_file.xlsx'

            # Open a file and write the binary content of the response to it
            with open(suggested_filename, 'wb') as f:
                f.write(response.content)

            print(f"Downloaded file: {suggested_filename}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    # Scrape Singapore inflation data and print a summary
    print("\nSummary of Singapore Inflation Data:")
    SG_Inflation()

if __name__ == '__main__':
    main()