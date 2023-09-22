from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import pandas as pd
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
import mysql.connector as sql
from sqlalchemy import create_engine, text
import os

def waiting2(remaining_time):
    while remaining_time > 0:
        if remaining_time == 5:
            print(f"Waiting...", end=" ")
        if remaining_time <= 5:
            print(" " + str(remaining_time) + "... ", end='')
        if remaining_time == 1:
            print(" Passed ✅\n", end='')
        time.sleep(1)
        remaining_time -= 1

def initialize_webdriver():
    # Driver Path
    driver_path = "/Users/mac/Documents/chromedriver-mac-x64/chromedriver"

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless mode

    # Create a webdriver instance using the Service object
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    return driver

def current_time():
    # Get current date and time
    now = datetime.now()
    formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    filename_date = now.strftime("%Y-%m-%d")
    return formatted_date_time, filename_date

def scrape_inflation_data(driver, num_pages, formatted_date_time):
    n = 1
    No = []
    date = []  # Use to keep date
    inflation_data = []  # Use to keep inflation rate data
    year = []
    month = []
    value = []
    country_val = []
    source_val = []
    update_frequency_val = []
    status_val = []
    access_date_val = []
    publish_date_val = []
    link_val = []
    note_val = []

    # For Database MySQL
    country = "Indonesia"
    source = "Bank Indonesia"
    updateFrequency = "Monthly"
    status = "Real"
    accessDate = formatted_date_time
    publishDate = None
    link = "https://www.bi.go.id/en/statistik/indikator/data-inflasi.aspx"
    note = "Just show only month"

    for page in range(1, num_pages + 1):
        tr_elements = driver.find_elements(By.XPATH,
                                           '/html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div/div[2]/div[1]/div/div[1]/div[4]/table/tbody/tr')
        num_tr_tags = len(tr_elements)

        if page >= 1 and num_tr_tags in [9, 10]:
            for tr in range(1, 11 if num_tr_tags == 10 else 10):
                td_elements_1 = driver.find_element(By.XPATH,
                                                    f'/html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div/div[2]/div[1]/div/div[1]/div[4]/table/tbody/tr[{tr}]/td[1]')
                td_elements_2 = driver.find_element(By.XPATH,
                                                    f'/html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div/div[2]/div[1]/div/div[1]/div[4]/table/tbody/tr[{tr}]/td[2]')

                month_year = td_elements_1.text.split()
                month_part = month_year[0]
                year_part = month_year[1]

                # Value or inflation is the same.
                date.append(td_elements_1.text)
                inf_data = td_elements_2.text.replace(" %", "")
                inflation_data.append(inf_data)
                year.append(year_part)
                month.append(month_part)
                value.append(inf_data)
                country_val.append(country)
                source_val.append(source)
                update_frequency_val.append(updateFrequency)
                status_val.append(status)
                access_date_val.append(accessDate)
                publish_date_val.append(publishDate)
                link_val.append(link)
                note_val.append(note)
                No.append(n)
                n += 1

            # Go to next page by pressing `ENTER` key
            next_button = driver.find_element(By.CLASS_NAME, 'next')
            next_button.send_keys(Keys.ENTER)

            # Waiting 5s for the next page!
            waiting2(remaining_time=5)

    return No, inflation_data, year, month, value, country_val, source_val, update_frequency_val, status_val, \
           access_date_val, publish_date_val, link_val, note_val


def store_in_database(
        inflation_data, year, month, value, country_val, source_val,
        update_frequency_val, status_val, access_date_val, publish_date_val, link_val, note_val):

    db_config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'LaySENG./333',
        'database': 'MoLVT'
    }
    conn = sql.connect(**db_config)
    cursor = conn.cursor()

    create_table_query = '''
            CREATE TABLE IF NOT EXISTS indonesia_inflation_sample (
                No INT AUTO_INCREMENT PRIMARY KEY,
                Country VARCHAR(20),
                Source VARCHAR(50),
                UpdateFrequency VARCHAR(20),
                Status VARCHAR(10),
                Year INT,
                Month VARCHAR(15),
                Value FLOAT,
                AccessDate DATETIME,
                PublishDate VARCHAR(255),
                Link VARCHAR(255),
                Note VARCHAR(255)
            );
        '''
    cursor.execute(create_table_query)

    for i in range(0, len(inflation_data)):
        check_query = '''
            SELECT 1 FROM indonesia_inflation_sample WHERE Year = %s AND Month = %s;
        '''
        cursor.execute(check_query, (year[i], month[i]))
        result = cursor.fetchone()

        if not result:
            # Data does not exist, so insert it
            insert_query = '''
                    INSERT INTO indonesia_inflation_sample (Country, Source, UpdateFrequency, Status,
                    Year, Month, Value, AccessDate, PublishDate, Link, Note) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s);
            '''
            listing_columns = (country_val[i], source_val[i], update_frequency_val[i], status_val[i], year[i], month[i],
                               value[i], access_date_val[i], publish_date_val[i], link_val[i], note_val[i])

            cursor.execute(insert_query, listing_columns)

    conn.commit()
    cursor.close()
    conn.close()

    return True

def dataframe():
    engine = create_engine(url="mysql+mysqlconnector://root:LaySENG./333@localhost/MoLVT", pool_recycle=3600)
    conn = engine.connect()

    query = text("SELECT * FROM indonesia_inflation_sample WHERE Year = 2022;")
    result = conn.execute(query)
    all_cols = result.keys()
    columns = []
    for col in all_cols:
        columns.append(col)

    df = pd.DataFrame(result.fetchall(), columns=columns)

    path = "/Users/mac/Desktop/MoLVC Internship/Data-management-system-ministry/processing/scrape/IndoInflation/DB_Data/"
    filename = "IndoInfDB.xlsx"
    file_path = path + filename
    try:
        df.to_excel(os.path.join(path, filename), index=False)
        if os.path.exists(file_path):
            print(f"\nData saved at `{file_path}`\n")
    except Exception as e:
        print(f"\nAn error occurred while saving the data: {str(e)}\n")

    conn.close()
    return df

def main():
    # # URL of the page
    # url = "https://www.bi.go.id/en/statistik/indikator/data-inflasi.aspx"
    #
    # # Get current date and time
    # now = datetime.now()
    # formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    # filename_date = now.strftime("%Y-%m-%d")
    #
    # driver = initialize_webdriver()
    # driver.get(url)
    #
    # # page_input = int(input("How many pages do you want to scrape?: "))
    # page_input = 4
    #
    # No, inflation_data, year, month, value, country_val, source_val, update_frequency_val, status_val, access_date_val, \
    # publish_date_val, link_val, note_val = scrape_inflation_data(driver=driver, num_pages=page_input, formatted_date_time=formatted_date_time)
    #
    # # Check DB after scraping and storing in DB
    # if (store_in_database(
    #         inflation_data, year, month, value, country_val, source_val,
    #         update_frequency_val, status_val, access_date_val, publish_date_val, link_val, note_val) == True):
    #     print("\nThe data is stored in the database and updated accordingly!")
    # else:
    #     print("\nThe data is not stored in the database and updated accordingly!")

    print(dataframe())

    # driver.quit()

if __name__ == "__main__":
    main()
