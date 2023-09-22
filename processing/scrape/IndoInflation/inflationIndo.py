from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import mysql.connector as sql
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime

def waiting2():
    max_timeout = 5
    remaining_time = max_timeout

    while remaining_time > 0:
        if remaining_time == 5:
            print(f"Waiting...", end=" ")
        if remaining_time <= 5:
            print(" " + str(remaining_time) + "... ", end='')
        if remaining_time == 1:
            print(" Passed ✅\n", end='')
        time.sleep(1)
        remaining_time -= 1

def inflation_indonesia():
    # URL of the page
    url = "https://www.bi.go.id/en/statistik/indikator/data-inflasi.aspx"

    # Driver Path
    driver_path = "/Users/mac/Documents/chromedriver-mac-x64/chromedriver"

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless mode

    # Create a Service object
    service = Service(driver_path)

    # Create a webdriver instance using the Service object
    driver = webdriver.Chrome(service=service)

    driver.get(url)

    # Get current date and time
    now = datetime.now()
    # Format the date and time
    formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    filename_date = now.strftime("%Y-%m-%d")

    # For DataFrame
    No = []
    columns = []  # Use to keep headers
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

    '''
        Because of it has <thead> and inside <thead> has <tr> which contains columns name. 
        So, I need to specify it first.   
    '''
    th_elements_1 = driver.find_element(By.XPATH,
                                        f'//*[@id="tableData"]/table/thead/tr/th[1]')
    th_elements_2 = driver.find_element(By.XPATH,
                                        f'//*[@id="tableData"]/table/thead/tr/th[2]')
    columns.append(th_elements_1.text)
    columns.append(th_elements_2.text)

    # page_input = int(input("How many pages ypu want?: "))
    page_input = 2
    n = 1

    for page in range(1, page_input + 1):

        # Count tag in each page first before start scraping data, to avoid error on each page while scraping.
        tr_elements = driver.find_elements(
            By.XPATH,
            '/html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div/div[2]/div[1]/div/div[1]/div[4]/table/'
            'tbody/tr'
        )
        # Check the number of <tr> tags found
        num_tr_tags = len(tr_elements)

        if page >= 1 and num_tr_tags == 10:
            for tr in range(1, 11):  # Set fixed amount of <tr> in each page

                # In this section, I start pulling data from <tbody> which contains 10 <tr> tags as well.
                td_elements_1 = driver.find_element(
                    By.XPATH,
                    f'/html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div/div[2]/div[1]/div/div[1]/div[4]/'
                    f'table/tbody/tr[{tr}]/td[1]')
                td_elements_2 = driver.find_element(
                    By.XPATH,
                    f'/html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div/div[2]/div[1]/div/div[1]/div[4]/'
                    f'table/tbody/tr[{tr}]/td[2]')

                # Split Month and Year from each other
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
            next_button = driver.find_element(
                By.CLASS_NAME, f'next')
            next_button.send_keys(Keys.ENTER)

            # Waiting 5s for the next page!
            waiting2()

        elif page >= 1 and num_tr_tags == 9:
            for tr in range(1, 10):  # Set fixed amount of <tr> in each page

                # In this section, I start pulling data from <tbody> which contains 10 <tr> tags as well.
                td_elements_1 = driver.find_element(
                    By.XPATH,
                    f'/html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div/div[2]/div[1]/div/div[1]/div[4]/'
                    f'table/tbody/tr[{tr}]/td[1]')
                td_elements_2 = driver.find_element(
                    By.XPATH,
                    f'/html/body/form/div[12]/div/div[3]/div[2]/div[4]/div/div[1]/div/div[2]/div[1]/div/div[1]/div[4]/'
                    f'table/tbody/tr[{tr}]/td[2]')

                # Split Month and Year from each other
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
            next_button = driver.find_element(
                By.CLASS_NAME, f'next')
            next_button.send_keys(Keys.ENTER)

            # Waiting 5s for the next page!
            waiting2()

    # print(len(No))
    # print(len(country_val))
    # print(len(source_val))
    # print(len(update_frequency_val))
    # print(len(status_val))
    # print(len(year))
    # print(len(month))
    # print(len(inflation_data))
    # print(len(access_date_val))
    # print(len(publish_date_val))
    # print(len(link_val))
    # print(len(note_val))

    # DataFrame
    df = pd.DataFrame(data={
        "No.": No,
        "Country": country_val,
        "Source": source_val,
        "Update frequency": update_frequency_val,
        "Status": status_val,
        "Year": year,
        "Month": month,
        "Value": inflation_data,
        "Access Date": access_date_val,
        "Publish Date": publish_date_val,
        "Link": link_val,
        "Note": note_val
        },
        columns=['No.', "Country", "Source", "Update frequency", "Status", "Year", "Month", "Value", "Access Date", "Publish Date", "Link", "Note"]
    )

    path = "/Users/mac/Desktop/MoLVT/Indo Inflation"
    df.to_csv(path + "/IndoInflation" + filename_date + ".csv", index=False)

    print("\n")
    print(df)

    """######################### Database - HERE WE GO! #########################"""
    # Start Storing in Database Process
    db_config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'LaySENG./333',
        'database': 'MoLVT'
    }
    conn = sql.connect(**db_config)
    cursor = conn.cursor()

    # Create a table
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
            )
        '''
    cursor.execute(create_table_query)

    # Inside the loop where we insert data
    for i in range(0, len(inflation_data)):
        # Check if the data already exists based on 'year' and 'month'
        check_query = '''
                SELECT 1 FROM indonesia_inflation_sample
                WHERE Year = %s AND Month = %s
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
            listing_columns = (country, source, updateFrequency, status, year[i], month[i],
                               value[i], accessDate, publishDate, link, note)

            cursor.execute(insert_query, listing_columns)

    # Commit changes
    conn.commit()

    # Write a SQL query to select the data
    query = f"SELECT * FROM indonesia_inflation_sample;"
    cursor.execute(query)
    results = cursor.fetchall()
    # Check if the results are empty
    if not results:
        print("\nThe data is not stored in the database!")
    else:
        print("\nThe data is stored in the database and updated accordingly!")

    # Close the cursor and connection
    cursor.close()
    conn.close()

    driver.quit()


inflation_indonesia()
