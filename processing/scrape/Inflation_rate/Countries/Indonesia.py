import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import mysql.connector as sql
from sqlalchemy import text
from processing.constant import user, internationalIFR_table, database_name, host, password, engine

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", 5)


def waiting2(remaining_time):
    """
    Wait for a specified amount of time while displaying countdown messages.

    Parameters:
    remaining_time (int): The maximum time to wait for a new page.

    This function waits for the specified amount of time while displaying countdown messages. It prints "Waiting..."
    when 5 seconds are remaining, counts down from 5 to 1, and prints "Passed ✅" when the waiting is complete.
    """
    while remaining_time > 0:
        if remaining_time == 5:
            print("Waiting...", end=" ")
        if remaining_time <= 5:
            print(" " + str(remaining_time) + "... ", end='')
        if remaining_time == 1:
            print(" Passed ✅\n", end='')
        time.sleep(1)
        remaining_time -= 1


def initialize_webdriver():
    """
    :return: `driver`: a variable defines the value which is retrieve from Chrome Service.
    """

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless mode

    # Create a webdriver instance using the Service object
    driver = webdriver.Chrome()
    return driver


def current_time():
    """
    :return: `formatted_date_time`: represented time of access date.
             `filename_date` (Optional): use with `pandas.to_csv()` for naming filename.
    """
    # Get current date and time
    now = datetime.now()
    formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    filename_date = now.strftime("%Y-%m-%d")
    return formatted_date_time, filename_date


def scrape_inflation_data(driver, num_pages, formatted_date_time):
    """
    :param num_pages:
    :param driver:
    :param formatted_date_time: :param num_pages: :param driver: :return: all return variables has type `list`,
    in order to use with dataframe and any further use. `No`. `inflation_data`, `year`, `month`, `value`,
    `country_val`, `source_val`, `update_frequency_val`, `status_val`, `access_date_val`, `publish_date_val`,
    `link_val`, `note_val`
    """
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
        tr_elements = driver.find_elements(
            By.XPATH,
            '/html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div/div[2]/div[1]/div/div[1]/div['
            '4]/table/tbody/tr')
        num_tr_tags = len(tr_elements)

        if page >= 1 and num_tr_tags in [9, 10]:
            for tr in range(1, 11 if num_tr_tags == 10 else 10):
                td_elements_1 = driver.find_element(
                    By.XPATH,
                    f'/html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div/div[2]/div[1]/div/div[1]/div['
                    f'4]/table/tbody/tr[{tr}]/td[1]')
                td_elements_2 = driver.find_element(
                    By.XPATH,
                    f'/html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div/div[2]/div[1]/div/div[1]/div['
                    f'4]/table/tbody/tr[{tr}]/td[2]')

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
        your_host, your_user, your_password, your_database, your_db_table,
        inflation_data, year, month, value, country_val, source_val,
        update_frequency_val, status_val, access_date_val, publish_date_val, link_val, note_val):
    """
    All parameters here is same as the return variables from the previous function,
        `scrape_inflation_data()`.

    :param note_val:
    :param link_val:
    :param publish_date_val:
    :param access_date_val:
    :param status_val:
    :param update_frequency_val:
    :param source_val:
    :param country_val:
    :param value:
    :param month:
    :param year:
    :param inflation_data:
    :param your_db_table:
    :param your_database:
    :param your_password:
    :param your_user:
    :param your_host:
    :return: `True`: `Bool`: Use to check in with DB whether it stored or not.
    """

    db_config = {
        'host': f'{your_host}',
        'user': f'{your_user}',
        'password': f'{your_password}',
        'database': f'{your_database}'
    }
    conn = sql.connect(**db_config)
    cursor = conn.cursor()

    create_table_query = f'''
            CREATE TABLE IF NOT EXISTS {your_db_table} (
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
        check_query = f'''
            SELECT 1 FROM {your_db_table} WHERE Year = %s AND Month = %s AND Country = %s;
        '''
        cursor.execute(check_query, (year[i], month[i], country_val[i]))
        result = cursor.fetchone()
        if not result:
            # Data does not exist, so insert it
            insert_query = f'''
                    INSERT INTO {your_db_table} (Country, Source, UpdateFrequency, Status,
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


def dataframe(your_db_table, your_db_condition):
    """
    We use `SQLAlchemy` to access the data from Database into DataFrame.
    TODO:
        - Open up the terminal or cmd (Command Prompt)
            `pip install sqlalchemy`

    :return: `df`: DataFrame from MySQL Database.
    """
    conn = engine.connect()

    query = text(f"SELECT * FROM {your_db_table} WHERE {your_db_condition};")
    result = conn.execute(query)

    all_cols = result.keys()
    columns = []
    for col in all_cols:
        columns.append(col)

    df = pd.DataFrame(result.fetchall(), columns=columns)

    # path = r"/Users/mac/Desktop/MoLVC Internship/Data-management-system-ministry/processing/scrape/IndoInflation/DB_Data/"
    # filename = "IndoInfDB.xlsx"
    # file_path = path + filename
    # try:
    #     df.to_excel(os.path.join(path, filename), index=False)
    #     if os.path.exists(file_path):
    #         print(f"\nData saved at `{file_path}`\n")
    # except Exception as e:
    #     print(f"\nAn error occurred while saving the data: {str(e)}\n")
    #
    # conn.close()
    return df


def read_db(your_host, your_user, your_password, your_database, your_db_table, your_db_condition, Source, Indicator,
            UpdateFrequency, Unit, Title):
    # Replace these with your own database credentials and SQL query
    db_config = {
        'host': f'{your_host}',
        'user': f'{your_user}',
        'password': f'{your_password}',
        'database': f'{your_database}'
    }

    # Define your SQL query
    sql_query = f"SELECT * FROM {your_db_table} WHERE {your_db_condition};"

    # Use the engine to execute the query andti read the result into a DataFrame
    df = pd.read_sql(sql_query, con=engine)

    # Close the database connection
    engine.dispose()

    # Close the database connection
    engine.dispose()

    base_col = ['No.', 'Title', 'Country', 'Source', 'Update frequency', 'Status',
                'Year', 'Month', 'Indicator', 'Sub 1', 'Sub 2', 'Sub 3', 'Sub 4',
                'Sub 5', 'Sub 6', 'Unit', 'Value', 'Access Date', 'Publish Date',
                'Link (if available)', 'Note', 'Note.1']

    df.rename(columns={'No': 'No.', 'AccessDate': 'Access Date', 'PublishDate': 'Publish Date',
                       'Link': 'Link (if available)'}, inplace=True)

    missing_cols = [col for col in base_col if col not in df.columns]
    print(missing_cols)
    nrow = df.shape[0]
    for i, col in enumerate(missing_cols):
        df[col] = [
            [Title] * nrow,
            [UpdateFrequency] * nrow,
            [Indicator] * nrow,
            ['NaN'] * nrow,
            ['NaN'] * nrow,
            ['NaN'] * nrow,
            ['NaN'] * nrow,
            ['NaN'] * nrow,
            ['NaN'] * nrow,
            [Unit] * nrow,
            ['NaN'] * nrow][i]

    # path = '/Users/mac/Desktop/MoLVC Internship/Data-management-system-ministry/processing/scrape/IndoInflation/DB_Data/'
    # df[base_col].to_excel(path + 'indonesia_inflation.xlsx', index=False)
    # df[base_col].to_csv(path + 'indonesia_inflation.csv', index=False)

    return df[base_col]


def main(driver):
    your_host = host
    your_user = user
    your_password = password
    your_database = database_name
    your_db_table = internationalIFR_table
    your_db_condition = 'Year = 2022'

    # URL of the page
    url = "https://www.bi.go.id/en/statistik/indikator/data-inflasi.aspx"

    # Get current date and time
    now = datetime.now()
    formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    filename_date = now.strftime("%Y-%m-%d")

    # Initialize Webdriver
    driver.get(url)

    # Page amounts
    # page_input = int(input("How many pages do you want to scrape?: "))
    page_input = 1

    """ 
    All these 13 Variables is the return variables from 
        `scrape_inflation_data(driver=driver, num_pages=page_input, formatted_date_time=formatted_date_time)` 
    """
    No, inflation_data, year, month, value, country_val, source_val, update_frequency_val, status_val, access_date_val, \
        publish_date_val, link_val, note_val = scrape_inflation_data(driver=driver, num_pages=page_input,
                                                                     formatted_date_time=formatted_date_time)

    # Check DB after scraping and storing in DB
    if (store_in_database(your_host, your_user, your_password, your_database, your_db_table,
                          inflation_data, year, month, value, country_val, source_val,
                          update_frequency_val, status_val, access_date_val, publish_date_val, link_val,
                          note_val) != True):
        print("\nThe data is not stored in the database and updated accordingly!")
    else:
        print("\nThe data is stored in the database and updated accordingly!")

    # Show dataframe
    print(dataframe(your_db_table=your_db_table, your_db_condition=your_db_condition))

    # read_DB() function
    print(
        read_db(
            your_host=your_host, your_user=your_user, your_password=your_password,
            your_database=your_database, your_db_table=your_db_table, your_db_condition=your_db_condition,
            Source="Bank Indonesia", Indicator="Inflation", UpdateFrequency="Monthly",
            Unit='Percentage', Title="Inflation Rate"
        )
    )

