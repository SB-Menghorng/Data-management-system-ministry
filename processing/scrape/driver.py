from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


class WebDriverHandler(webdriver.Chrome):
    """
   The `WebDriverHandler` class provides methods for web scraping a specific website using Selenium.

   Attributes:
       teardown (bool): Whether to quit the WebDriver on exit.

   Methods:
       get_xml(self):
           Scrapes the website to extract XML download links.

       extract_file(self, option, indicator):
           Extracts data from an XML file and processes it based on the selected option and indicator.

       database_connection(self, option=None, indicator=None, create_table=True, table_show=False, delete_table=False, insert_data=False):
           Stores extracted data in a database table with optional table management operations.

   Use Case:
       The `Scraper` class simplifies web scraping tasks using Selenium and facilitates data extraction,
       processing, and database storage.

   """

    def __init__(self, teardown=False):
        """
       Initializes a web scraper using Selenium for a specific website.

       Parameters:
       destination_dir (str): The directory where downloaded files will be stored.
       driver (str): The path to the Chrome WebDriver executable.
       teardown (bool): Whether to quit the WebDriver on exit.

       This class extends the webdriver.Chrome class from Selenium to facilitate web scraping.
       It sets up the WebDriver with specific options and provides methods for data extraction.
       """
        self.service = ChromeService(ChromeDriverManager().install())
        self.teardown = teardown
        chrome_options = webdriver.ChromeOptions()
        super(WebDriverHandler, self).__init__(options=chrome_options)
        self.implicitly_wait(3)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Handles the WebDriver cleanup on context exit.

        Parameters:
        exc_type: The type of exception raised (if any).
        exc_val: The exception value.
        exc_tb: The exception traceback.

        If the 'teardown' flag is set to True, this method will quit the WebDriver.
        """
        if self.teardown:
            self.quit()
