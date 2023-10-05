import pandas as pd
from datetime import datetime
from processing.connection.database import Database
from processing.constant import host, user, internationalIFR_table, database_name, password

current_year = datetime.now().year


def Inflation_rate(end_year):
    """
    Scrape and process inflation rate data for the Philippines.

    Parameters:
    end_year (int): The end year for data retrieval.

    Returns:
    pd.DataFrame: Processed inflation rate data in a DataFrame.
    """
    base_url = "https://www.bsp.gov.ph/Statistics/Prices/"
    links2 = []

    for i in range(2000, end_year + 1, 6):
        if i == 2000:
            url = f'{base_url}prices{i}'
        elif i == 2006:
            url = f'{base_url}infrate.xls'
        else:
            url = f'{base_url}infrate{i}.xls'
        links2.append(url)

    # Read data from the latest link
    data = pd.read_excel(links2[-1], sheet_name='Monthly')

    # Data cleaning
    df_cleaned = data.dropna(how='all')
    df_cleaned = df_cleaned.dropna(axis=1, how='all')
    df_cleaned = df_cleaned.dropna(how='all')
    df_cleaned = df_cleaned.reset_index(drop=True)
    df_cleaned = df_cleaned.drop([0, 1, 2, 3])
    df_cleaned.columns = ['year', 'month', 'inflation_rate']
    df_cleaned = df_cleaned.iloc[1:]  # Remove the first row
    df_cleaned = df_cleaned.reset_index(drop=True)
    df_cleaned = df_cleaned.dropna(subset=[col for col in df_cleaned.columns if df_cleaned[col].dtype == object])

    # Create a formal DataFrame
    df_formal = pd.DataFrame({
        "No": df_cleaned.index,
        "Country": "Philippines",
        "Source": "Central_Bank_of_the_Philippines",
        "Update_frequency": "Monthly",
        "Status": "Real",
        "Year": df_cleaned['year'],
        "Month": df_cleaned['month'],
        "Indicator": "Inflation",
        "Value": df_cleaned['inflation_rate'],
        "Access_Date": datetime.now(),
        "Publish_Date": "",
        "Link(if_available)": "https://www.bsp.gov.ph/SitePages/Statistics/Prices.aspx?TabId=8",
        "Note": "Base 2018 = 100"
    })
    df_formal.rename(columns=dict(zip(df_formal.columns[1:],
                                      ['Country', 'Source', 'Update frequency', 'Status', 'Year', 'Month', 'Indicator',
                                       'Value', 'Publish Date', 'Access_Date', 'Link', 'Note'])), inplace=True)
    return df_formal[['Country', 'Source', 'Update frequency', 'Status', 'Year', 'Month', 'Indicator',
                      'Value', 'Publish Date', 'Access_Date', 'Link', 'Note']]


def main():
    db = Database(host, password, user, table=internationalIFR_table, database=database_name)
    # db.create_table()
    df = Inflation_rate(current_year)
    df = df[df['Year'] >= 2018]
    # db.insert_data(df)
    db.show_table()
    return df


