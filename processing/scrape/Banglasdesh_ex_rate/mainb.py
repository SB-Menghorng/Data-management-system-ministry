from processing.scrape.Banglasdesh_ex_rate.scrapers.ex_rate_banglasdesh import ExchangeRateScraperbb
from processing.constant import driver_path
import os

class Banglasdesh:
    def __init__(self, path):
        self.path = path
        # self.driver_path = driver_path  # Renamed class attribute

    def mainbd(self,path,input_date_str,driver_path=driver_path):
        target_currency = "USD"
        driver_path=driver_path
        scraper = ExchangeRateScraperbb(driver_path)

        exchange_rate_data = scraper.scrape_exchange_rate(target_currency, input_date_str)

        destination_dir = path
        # Create the destination directory if it doesn't exist
        os.makedirs(destination_dir, exist_ok=True)
        # Define the CSV file name based on input_date_str
        csv_filenameb = f"BangEx_rate{input_date_str}.csv"
        # Construct the full path to the CSV file
        csv_filepathb = os.path.join(destination_dir, csv_filenameb)
        # Save the scraped data to the CSV file
        exchange_rate_data.to_csv(csv_filepathb, index=False)
        print(f"Data saved to {csv_filepathb}")
