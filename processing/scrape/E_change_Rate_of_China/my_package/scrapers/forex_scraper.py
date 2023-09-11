from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
from datetime import datetime

class ForexScraper:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.service = Service(executable_path=self.driver_path)
        self.browser = webdriver.Chrome(executable_path=self.driver_path)


    def scrape_data(self,target_currency, start_date, end_date):
        url = 'https://www.boc.cn/sourcedb/whpj/enindex2.htm'
        self.browser.get(url)
        self.browser.maximize_window()

        iframe_element = self.browser.find_element(By.XPATH, '//*[@id="DataList"]')
        self.browser.switch_to.frame(iframe_element)

        button_start = self.browser.find_element(By.XPATH, '//*[@id="historysearchform"]/input[1]')
        button_end = self.browser.find_element(By.XPATH, '//*[@id="historysearchform"]/input[2]')
        wait = WebDriverWait(self.browser, 10)
        select_button = wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="historysearchform"]/select')))
        #select_button = self.browser.find_element(By.XPATH, '//*[@id="historysearchform"]/select')
        select_button.send_keys(target_currency)
        button_start.send_keys(start_date)
        button_end.send_keys(end_date)

        search_button = self.browser.find_element(By.XPATH, '//*[@id="historysearchform"]/input[3]')
        search_button.click()

        data = []
        # for n in range(num_pages):
        #     print("Scrapped page", n + 1)
        # Get the total number of pages from the page information
        page_info = wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="list_navigator"]/span[1]')))
        total_pages = int(page_info.find_element(By.CLASS_NAME, 'nav_pagenum').text)
            # Handle the error here, e.g., by waiting and retrying or exiting gracefully.
        print("Number of Total pages in this interval are # ", total_pages)
        # print("Number of Total pages in this interval ",total_pages)
        for n in range(total_pages):
            # print("Scrapped page", n + 1)
            # n=n+1
            wait = WebDriverWait(self.browser, 10)
            try:
                # Wait for the table to be present
                table = wait.until(ec.presence_of_element_located((By.XPATH, "/html/body/table[2]")))

                rows = table.find_elements(By.TAG_NAME, value="tr")
                for i, row in enumerate(rows):
                    if i == 0:
                        continue
                    cells = row.find_elements(By.TAG_NAME, value="td")
                    if len(cells) >= 7:
                        currency_name = cells[0].text
                        buying_rate = cells[1].text
                        cash_buying_rate = cells[2].text
                        selling_rate = cells[3].text
                        cash_selling_rate = cells[4].text
                        middle_rate = cells[5].text
                        pub_time = cells[6].text

                        data.append([currency_name, buying_rate, cash_buying_rate, selling_rate,
                                     cash_selling_rate, middle_rate, pub_time])
                        print(
                            f"Currency: {currency_name}, Buying Rate: {buying_rate}, Cash_buying_rate :{cash_buying_rate}, "
                            f"Selling Rate: {selling_rate}, Cahs_selling_rate : {cash_selling_rate}, Middle_rate : {middle_rate}, "
                            f"Pub Time: {pub_time}")
                        # pub_time_date = datetime.strptime(pub_time, "%Y.%m.%d %H:%M:%S").strftime("%y-%m-%d")
                        # if pub_time_date < start_date:
                            # break
                try:
                    button_next = wait.until(
                        ec.element_to_be_clickable((By.XPATH, '//*[@id="list_navigator"]/span[3]/a')))
                    button_next.click()
                except (TimeoutException, NoSuchElementException):
                    print("No 'Next' button found or it's not clickable.")
                    break  # Exit the loop if 'Next' button is not found

            except TimeoutException:
                print("Timeout occurred while waiting for elements to load.")
                break  # Exit the loop if timeout occurs

        self.browser.quit()
        columns = ["Currency Name", "Buying Rate", "Cash Buying Rate", "Selling Rate", "Cash Selling Rate",
                   "Middle Rate", "Pub Time"]
        df = pd.DataFrame(data, columns=columns)
        return df