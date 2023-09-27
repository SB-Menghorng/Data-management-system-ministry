## Interface
# Put your current path directory here for assets folder.
from sqlalchemy import create_engine

static_folder = r"D:\Intership\Labour ministry of combodain\system\processing\templates\assets"

## Scraping
# Driver test path:
driver_path = r"D:\Intership\Labour ministry of combodain\chromedriver-win64\chromedriver.exe"

# Path of Streamlit file (e.g., streamlit_app.py file)
psf = r"D:\Intership\Labour ministry of combodain\system\streamlit_app.py"

# User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}

## Visualization
# Add the directory path for Thyda Streamlit testing
thyda_dir = r"D:\Intership\Labour ministry of combodain\test\SampleSpreadSheet.csv"

# File test
fltest = r"some_asean_and_european_currencies_against_khmer_riel_end_period.csv"

## Database
host = 'localhost'
user = 'root'
password = 'menghorng'
database_name = 'Economic'
your_table_name = 'Inflation'

# Create a SQLAlchemy engine for database connection
engine = create_engine(url=f"mysql+mysqlconnector://{user}:{password}@{host}/{database_name}", pool_recycle=3600)

## Excel
excel = r"D:\Intership\Labour ministry of combodain\test\DataSampleForChecking (2).xlsx"
sheet_name = "DatabaseSample"
