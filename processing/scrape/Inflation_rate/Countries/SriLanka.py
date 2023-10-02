import re
from datetime import datetime

import pandas as pd
from pandas.core.interchange import dataframe
from selenium.webdriver.common.by import By


class InflationRate:
    """
    The `InflationRate` class provides methods for scraping consumer price inflation data from the Central Bank of
    Sri Lanka.

    Attributes:
        driver: The Selenium WebDriver instance for web automation.

    Methods:
        __init__(self, driver):
            Initializes the InflationRate class with the specified Selenium WebDriver instance.

        scrape_inflation_data(self): Scrapes consumer price inflation data from the Central Bank of Sri Lanka website
        and returns it as a DataFrame.

    Use Case: The `InflationRate` class simplifies the process of scraping consumer price inflation data from a
    specific source.
    """
    def __init__(self, driver):
        self.driver = driver

    def scrape_inflation_data(self) -> dataframe:
        url = "https://www.cbsl.gov.lk/en/measures-of-consumer-price-inflation#"

        self.driver.get(url)
        iframe = self.driver.find_element(By.XPATH, '//*[@id="iFrameResizer3"]')

        self.driver.switch_to.frame(iframe)
        tables = self.driver.find_elements(By.TAG_NAME, 'table')

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

        return df1
