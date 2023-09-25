## Interface
# Put your current path directory here for assets folder.
from sqlalchemy import create_engine

static_folder = r"D:\Intership\Labour ministry of combodain\system\processing\templates\assets"

## Scraping
# driver test path:
driver_path = r"D:\Intership\Labour ministry of combodain\chromedriver-win64\chromedriver.exe"

# path of streamlit file (Ex: streamlit_app.py file)
psf = r"D:\Intership\Labour ministry of combodain\system\streamlit_app.py"

## Visualization
# add to directory of file for thyda streamlit testing
thyda_dir = r"D:\Intership\Labour ministry of combodain\test"

# file test

fltest = r"some_asean_and_european_currencies_against_khmer_riel_end_period.csv"

## Database
host = 'localhost'
user = 'root'
password = 'menghorng'
database_name = 'Economic'
your_table_name = 'Inflation'

engine = create_engine(url=f"mysql+mysqlconnector://{user}:{password}@{host}/{database_name}", pool_recycle=3600)

