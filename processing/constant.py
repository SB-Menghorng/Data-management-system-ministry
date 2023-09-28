from sqlalchemy import create_engine

# Put your current path directory here for assets folder.
static_folder = "/Users/mac/Desktop/MoLVC Internship/Data-management-system-ministry/processing/templates/assets"

# driver test path:
driver_path = "/Users/mac/Documents/chromedriver-mac-x64/chromedriver"

# path of streamlit file (Ex: streamlit_app.py file)
psf = "/Users/mac/Desktop/MoLVC Internship/Data-management-system-ministry/streamlit_app.py"

# add to directory of file for thyda streamlit testing
thyda_dir = "/Users/mac/Desktop/MoLVC Internship/Data-management-system-ministry/processing/visualizations/test"

# file test
fltest = r"some_asean_and_european_currencies_against_khmer_riel_end_period.csv"

your_host = 'localhost'
your_user = 'root'
your_password = 'LaySENG./333'
your_database = 'MoLVT'
your_db_table = 'indonesia_inflation_sample'
your_db_condition = 'Year = 2022'

engine = create_engine(url=f"mysql+pymysql://{your_user}:{your_password}@{your_host}/{your_database}",
                       pool_recycle=3600)

path_file_DB = "/Users/mac/Desktop/MoLVC Internship/Data-management-system-ministry/processing/scrape/IndoInflation/DB_Data/"


