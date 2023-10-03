from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


class WebDriverHandler(webdriver.Chrome):
    """
    The `WebDriverHandler` class provides methods for web scraping a specific website using Selenium.

    Attributes:
        teardown (bool): Whether to quit the WebDriver on exit.

    Methods:
        __init__(self, teardown=False, download_dir=None):
            Initializes a web scraper using Selenium for a specific website.

        __exit__(self, exc_type, exc_val, exc_tb):
            Handles the WebDriver cleanup on context exit.

    Use Case:
        The `WebDriverHandler` class simplifies web scraping tasks using Selenium and facilitates data extraction,
        processing, and database storage.

    """

    def __init__(self, teardown=False, download_dir=None):
        """
       Initializes a web scraper using Selenium for a specific website.

       Parameters:
       destination_dir (str): The directory where downloaded files will be stored.
       driver (str): The path to the Chrome WebDriver executable.
       teardown (bool): Whether to quit the WebDriver on exit.

       This class extends the webdriver.Chrome class from Selenium to facilitate web scraping.
       It sets up the WebDriver with specific options and provides methods for data extraction.
       """
        try:
            self.service = ChromeService(ChromeDriverManager().install())
            self.teardown = teardown
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.page_load_strategy = 'eager'
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
            chrome_options.add_argument(f"user-agent={user_agent}")
            # chrome_options.add_argument("--headless")  # Run Chrome in headless mode
            if download_dir:
                chrome_options.add_experimental_option("prefs", {
                    "download.default_directory": download_dir
                })
            super(WebDriverHandler, self).__init__(options=chrome_options)
            # Set the detach option to True to keep the WebDriver running after script completion
            chrome_options.add_experimental_option("detach", True)
            self.implicitly_wait(5)
            self.maximize_window()
        except Exception as e:
            print(f"Error during initialization: {e}")
            # Handle the exception accordingly
            raise e  # Re-raise the exception if necessary

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Handles the WebDriver cleanup on context exit.

        Parameters:
        exc_type: The type of exception raised (if any).
        exc_val: The exception value.
        exc_tb: The exception traceback.

        If the 'teardown' flag is set to True, this method will quit the WebDriver.
        """
        try:
            if self.teardown:
                self.quit()
        except Exception as e:
            print(f"Error during cleanup: {e}")
            # Handle the exception accordingly
            raise e  # Re-raise the exception if necessary
