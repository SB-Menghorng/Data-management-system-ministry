def exp_sri_lanka(download_folder):
    """
    Download external sector data from the Central Bank of Sri Lanka's website.

    Args:
        download_folder (str): The directory where downloaded files will be saved.

    Returns:
        None

    This function scrapes data download links from the Central Bank of Sri Lanka's website
    and downloads the specified number of files into the provided download folder.
    """
    from bs4 import BeautifulSoup
    import requests
    url = 'https://www.cbsl.gov.lk/en/statistics/statistical-tables/external-sector'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    soup.find_all("div", class_="block-inner clearfix")
    ol1 = soup.find_all("div", class_="field-items")

    links = []
    for div in ol1:
        for link in div.find_all("a", href=True):
            links.append(link['href'])

    exp_imp_trade_download_link = []
    for i in range(0, 6):
        exp_imp_trade_download_link.append(links[i])

    exp_list = [exp_imp_trade_download_link[i] for i in range(0, 2)]
    # ==============================================================
    import os
    # List of URLs
    urls = exp_list
    # # Specify the folder where you want to save the files
    # download_folder = '/content/gdrive/MyDrive/Data/Import_by_Sri_Lanka'

    # Create the folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Download files
    for url in urls:
        response = requests.get(url)
        file_name = os.path.join(download_folder, os.path.basename(url))

        with open(file_name, 'wb') as file:
            file.write(response.content)

        print(f"Downloaded: {file_name}")

    print("All files downloaded successfully.")
