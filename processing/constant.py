# @Interface
# Put your current path directory here for assets folder.
from sqlalchemy import create_engine

static_folder = r"D:\Intership\Labour ministry of combodain\system\processing\templates\assets"

# @Scraping
# Driver test path:
driver_path = r"D:\Intership\Labour ministry of combodain\chromedriver-win64\chromedriver.exe"

# @Streamlit
# Path of Streamlit file (e.g., DashboardVisualization.py file)
dashboard = r"D:\Intership\Labour ministry of combodain\system\DashboardVisualization.py"
excelDashboard = r"D:\Intership\Labour ministry of combodain\system\DatabasesManagement.py"

# User-Agent
headers = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}

# @Visualization
# Add the directory path for inflation rate Streamlit testing
Inflation = r"D:\Intership\Labour ministry of combodain\test\SampleSpreadSheet.csv"

# File test
fltest = r"some_asean_and_european_currencies_against_khmer_riel_end_period.csv"

# @Database Setup
host = 'localhost'
password = 'menghorng'
user = 'root'
database_name = 'Economic'
table_name1 = 'Inflation'
table_name2 = 'Consumer_Price_Index'

# Create a SQLAlchemy engine for database connection
engine = create_engine(url=f"mysql+mysqlconnector://{user}:{password}@{host}/{database_name}", pool_recycle=3600)

# @Excel
excel = r"D:\Intership\Labour ministry of combodain\test\DataSampleForChecking (2).xlsx"
sheet_name = "DatabaseSample"

# Excel FIle name on Inflation Domestic
excelName2 = (r"D:\Intership\Labour ministry of combodain\demo\DomesticData\NBC\monetary_and_financial_statistics_data"
              r"\14.contributiontoinflationjun-23_6926.xlsx")

excelPathConst = r"C:/Users/Acer/Downloads/Internship/Data.xlsx"
sheetNameConst = r"Sheet1"
