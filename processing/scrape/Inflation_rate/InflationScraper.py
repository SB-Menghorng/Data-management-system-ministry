import concurrent.futures
import pandas as pd

from processing.constant import host, password, user, your_table_name, database_name
from processing.connection.database import Database
from processing.scrape.Inflation_rate.Countries import (Vietnam, Indonesia, Japanes, Philippines, Singapore, SriLanka,
                                                        Thai, Lao)
from processing.scrape.operations.selenium_ import WebDriverHandler


# def InflationRate(year):
#     driver = WebDriverHandler()
#     db = Database(host, password, user, table=your_table_name, database=database_name)
#     # db.delete_table()
#     db.create_table()
#     Vietnam.Scraper(driver).database_connection()
#     driver.switch_to.window(driver.window_handles[-1])
#
#     df_jp = Japanes.InflationRateScraper(driver).extract_data()
#     driver.switch_to.window(driver.window_handles[-1])
#
#     Indonesia.main(driver)
#     driver.switch_to.window(driver.window_handles[-1])
#
#     driver.switch_to.window(driver.window_handles[-1])
#
#     df_sl = SriLanka.InflationRate(driver).scrape_inflation_data()
#
#     driver.switch_to.window(driver.window_handles[-1])
#
#     df_L = Lao.LaoInflationDataScraper(driver).scrape_inflation_data(year)
#     driver.switch_to.window(driver.window_handles[-1])
#     dfs_sp = Singapore.InflationRateScraper(driver).scrape_and_process_data()
#     for df_ in dfs_sp:
#         db.insert_data(df_)
#     df_pp = Philippines.main()
#
#     df_t = Thai.ThaiConsumerPriceScraper(driver).scrape_consumer_price_data()
#     df_concat = pd.concat([df_jp, df_pp, df_sl, df_L, df_t], ignore_index=True)
#     #
#     db.insert_data(df_concat)
#
#     db.show_table()


def InflationRate(year, option):
    db = Database(host, password, user, table=your_table_name, database=database_name)

    def scrape_vietnam():
        driver = WebDriverHandler()
        Vietnam.Scraper(driver).database_connection()
        driver.close()

    def scrape_japan():
        driver = WebDriverHandler()
        df1_jp = Japanes.InflationRateScraper(driver).extract_data()
        driver.close()
        return df1_jp

    def scrape_indonesia():
        driver = WebDriverHandler()
        Indonesia.main(driver)
        driver.close()

    def scrape_sri_lanka():
        driver = WebDriverHandler()
        df1_sl = SriLanka.InflationRate(driver).scrape_inflation_data()
        driver.close()
        return df1_sl

    def scrape_lao():
        driver = WebDriverHandler()
        df1_L = Lao.LaoInflationDataScraper(driver).scrape_inflation_data(year)
        driver.close()
        return df1_L

    def scrape_singapore():
        driver = WebDriverHandler()
        df1s_sp = Singapore.InflationRateScraper(driver).scrape_and_process_data()
        driver.close()
        return df1s_sp

    def scrape_philippines():
        df1_pp = Philippines.main()
        return df1_pp

    def scrape_thailand():
        driver = WebDriverHandler()
        df1_t = Thai.ThaiConsumerPriceScraper(driver).scrape_consumer_price_data()
        driver.close()
        return df1_t
    if option == 'Inflation Rate':

        with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
            future_to_function = {
                executor.submit(scrape_vietnam): "Vietnam",
                executor.submit(scrape_indonesia): "Indonesia",
                executor.submit(scrape_sri_lanka): "Sri Lanka",
                executor.submit(scrape_lao): "Lao",
                executor.submit(scrape_singapore): "Singapore",
                executor.submit(scrape_philippines): "Philippines",
                executor.submit(scrape_thailand): "Thailand"
            }

            results = {}
            for future in concurrent.futures.as_completed(future_to_function):
                country = future_to_function[future]
                try:
                    data = future.result()
                    results[country] = data
                except Exception as e:
                    results[country] = str(e)

            # Process results
            df_pp = results.get("Philippines")
            df_sl = results.get("Sri Lanka")
            df_L = results.get("Lao")
            df_t = results.get("Thailand")
            dfs_sp = results.get("Singapore")
            print(df_pp, df_sl, df_L, df_t)

            db.delete_table()
            db.create_table()
            for df_ in dfs_sp:
                db.insert_data(df_)

            df_concat = pd.concat([df_pp, df_sl, df_L, df_t], ignore_index=True)
            db.insert_data(df_concat)

            # Show the table or return the necessary dataframes
            db.show_table()
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future_to_function = {
                executor.submit(scrape_japan): "Japan",
            }

            results = {}
            for future in concurrent.futures.as_completed(future_to_function):
                country = future_to_function[future]
                try:
                    data = future.result()
                    results[country] = data
                except Exception as e:
                    results[country] = str(e)

            # Process results
            df_jp = results.get("Japan")
            db.insert_data(df_jp)
            print(df_jp)

            # Show the table or return the necessary dataframes
            db.show_table()




# InflationRate(2020)

