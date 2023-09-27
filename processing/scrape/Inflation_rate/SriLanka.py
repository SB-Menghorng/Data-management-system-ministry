from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from processing.constant import driver_path
import pandas as pd
from datetime import datetime
import re


def scrape_inflation_data():
    url = "https://www.cbsl.gov.lk/en/measures-of-consumer-price-inflation#"

    # Specify the path to ChromeDriver
    # chrome_driver_path = driver_path
    # chrome_service = ChromeService(chrome_driver_path)
    # driver = webdriver.Chrome(service=chrome_service)
    # Create ChromeOptions object
    chrome_options = Options()

    # Set headless mode
    chrome_options.add_argument("--headless")

    # Create a ChromeDriver instance with headless mode
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

    driver.get(url)
    iframe = driver.find_element(By.XPATH, '//*[@id="iFrameResizer3"]')

    driver.switch_to.frame(iframe)
    tables = driver.find_elements(By.TAG_NAME, 'table')

    # Create an empty list to store data
    data = []
    now = datetime.now()
    current_year = now.year  # Starting year

    # Add constant values
    country = "Sri Lanka"
    source = "Central Bank of Sri Lanka"
    update_frequency = "Monthly"
    status = "Real"
    link = url
    Publish_ate = "None"

    # Access date
    access_date = datetime.now().date()

    # Initialize the index (No.) to 1
    index = 1

    # Iterate through the tables
    for table in tables:
        # Extract the value from the first row and second cell as a custom column name
        custom_column_name = "Note"
        rows = table.find_elements(By.TAG_NAME, 'tr')
        if len(rows) > 0:
            cells = rows[0].find_elements(By.TAG_NAME, 'td')
            if len(cells) >= 2:
                custom_column_name = cells[1].text.strip()
                match = re.search("(\d{4}=100)", custom_column_name)
                if match:
                    custom_column_name = match.group(1)
        column_names = ["Month", "Value"]

        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows[2:]:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if len(cells) >= 2:
                # Extract the data from the two cells
                values = [cell.text.strip() for cell in cells[:2]]

                # Determine the year based on the month
                if "January" in values[0]:
                    current_year -= 1

                # Create a dictionary with custom column names and original columns
                data_row = {
                    "No.": index,  # Add the No. column with auto-incremented value
                    "Country": country,
                    "Source": source,
                    "Update frequency": update_frequency,
                    "Status": status,
                    "Year": current_year,
                    column_names[0]: values[0],
                    column_names[1]: values[1],
                    "Access Date": access_date,
                    "Publish Date": Publish_ate,
                    "Link": link,  # Add the link value here
                    "Note": f"CCPI({custom_column_name}) based Headline Inflation (Y-o-Y)"
                }
                data.append(data_row)
                index += 1  # Increment the index (No.)

    # Create a DataFrame from the list of dictionaries
    df1 = pd.DataFrame(data)
    df1 = df1[[column for column in df1 if column != 'Note'] + ['Note']]
    # df.to_csv('Sri_Lanka_Consumer_price_inflation.csv', index=False)

    # Close the WebDriver
    driver.quit()

    return df1

# driverPath = 'C:\\Download\\Internship\\chromedriver.exe'
# df = scrape_inflation_data()
# df.info()
