from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from processing.scrape.operations.selenium_ import WebDriverHandler


class Scraper(WebDriverHandler):

    def __init__(self):
        # self.driver = driver
        super().__init__()
        self.url = 'https://ec.europa.eu/eurostat/databrowser/view/EI_CPHI_M__custom_7638553/default/table?lang=en'

    def ExtractData(self):
        self.get(self.url)
        wait = WebDriverWait(self, 10)
        cookies = self.get_cookies()
        print(cookies)

        # Add the cookie to the WebDriver instance
        self.add_cookie(cookies[0])

        # Now you can navigate to the desired page with the added cookie
        self.get(self.url)

        center_col = wait.until(EC.presence_of_element_located((By.ID, "tableDiv")))
        print('Get class:', center_col)


# driver = WebDriverHandler()
# sc = Scraper()
# sc.ExtractData()
