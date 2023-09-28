from sqlalchemy import create_engine, text
import pandas as pd

your_host = 'localhost'
your_user = 'root'
your_password = 'LaySENG./333'
your_database = 'MoLVT'
your_db_table = 'indonesia_inflation_sample'
your_db_condition = 'Year = 2022'

def read_db(your_host, your_user, your_password, your_database, your_db_table, your_db_condition, Source, Indicator,
            UpdateFrequency, Unit, Title):
    # Replace these with your own database credentials and SQL query
    db_config = {
        'host': f'{your_host}',
        'user': f'{your_user}',
        'password': f'{your_password}',
        'database': f'{your_database}'
    }

    engine = create_engine("mysql+mysqlconnector://root:LaySENG./333@localhost/MoLVT")

    # Define your SQL query
    sql_query = f"SELECT * FROM {your_db_table} WHERE {your_db_condition};"

    # Use the engine to execute the query andti read the result into a DataFrame
    df = pd.read_sql(sql_query, con=engine)

    # Close the database connection
    engine.dispose()

    # Close the database connection
    engine.dispose()

    base_col = ['No.', 'Title', 'Country', 'Source', 'Update frequency', 'Status',
                'Year', 'Month', 'Indicator', 'Sub 1', 'Sub 2', 'Sub 3', 'Sub 4',
                'Sub 5', 'Sub 6', 'Unit', 'Value', 'Access Date', 'Publish Date',
                'Link (if available)', 'Note', 'Note.1']

    df.rename(columns={'No': 'No.', 'AccessDate': 'Access Date', 'PublishDate': 'Publish Date',
                       'Link': 'Link (if available)'}, inplace=True)

    missing_cols = [col for col in base_col if col not in df.columns]
    print(missing_cols)
    nrow = df.shape[0]
    for i, col in enumerate(missing_cols):
        df[col] = [
            [Title] * nrow,
            [Source] * nrow,
            [UpdateFrequency] * nrow,
            [Indicator] * nrow,
            ['NaN'] * nrow,
            ['NaN'] * nrow,
            ['NaN'] * nrow,
            ['NaN'] * nrow,
            ['NaN'] * nrow,
            ['NaN'] * nrow,
            [Unit] * nrow,
            ['NaN'] * nrow][i]

print(read_db(your_host=your_host, your_user=your_user, your_password=your_password,
        your_database=your_database, your_db_table=your_db_table, your_db_condition=your_db_condition,
        Source="Bank Indonesia", Indicator="Inflation", UpdateFrequency="Monthly",
        Unit='Percentage', Title="Inflation Rate"))
