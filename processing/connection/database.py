import mysql.connector as conn
import pandas as pd


class Database:
    def __init__(self, host, password, user, table=None, database=None):
        """
        Initialize the Database object with the host and password.

        Args:
            host (str): The hostname or IP address of the MySQL server.
            password (str): The password for the MySQL server.

        """
        self.host = host
        self.password = password
        self.user = user
        self.database = database
        self.table = table

    def connection(self):
        """
        Establish a connection to the MySQL server.

        Returns:
            mysql.connector.MySQLConnection: A connection to the MySQL server.
            mysql.connector.cursor.MySQLCursor: A cursor object for executing SQL queries.

        """
        database = self.database
        mydb = conn.connect(host=self.host, user=self.user, passwd=self.password, database=database)
        cursor = mydb.cursor()
        return mydb, cursor

    def create_database(self, database_name=None):
        """
        Create a new MySQL database if it doesn't exist.

        Args:
            database_name (str): The name of the database to be created.
        """
        mydb, cursor = self.connection()
        database_name = self.database

        if database_name is None:
            print("Database name is not provided. Please specify a database name.")
            return

        # Check if the database exists
        cursor.execute("SHOW DATABASES LIKE %s", (database_name,))
        database_exists = cursor.fetchone()

        if not database_exists:
            # Create the database if it doesn't exist
            cursor.execute(f"CREATE DATABASE {database_name}")
            print(f"Database '{database_name}' created successfully.")
        else:
            print(f"Database '{database_name}' already exists.")

        # Close the cursor and the connection
        cursor.close()
        mydb.close()

    def create_table(self, table_name=None):
        """
        Create a MySQL table if it doesn't exist.

        Args:
            table_name (str): The name of the table to create.

        """
        mydb, cursor = self.connection()

        if table_name is None:
            # If table_name is not provided, use the currently set table_name
            table_name = self.table
        # Define the SQL statement to create a table if it doesn't exist
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            No INT AUTO_INCREMENT PRIMARY KEY,
            Country VARCHAR(255),
            Source VARCHAR(255),
            UpdateFrequency VARCHAR(255),
            Status VARCHAR(255),
            Year INT,
            Month  VARCHAR(255),
            Value FLOAT,
            AccessDate DATETIME,
            PublishDate VARCHAR(255),
            Link VARCHAR(255),
            Note VARCHAR(255)
        )
        """
        # Execute the SQL statement to create the table
        cursor.execute(create_table_query)
        print(f"Table '{table_name}' created successfully or already exists.")

        # Don't forget to commit the changes and close the connection when you're done
        mydb.commit()
        cursor.close()
        mydb.close()

    def insert_data(self, df):
        """
        Insert data from a DataFrame into a MySQL table.

        Args:
            df (pandas.DataFrame): The DataFrame containing the data to be inserted
        """
        mydb, cursor = self.connection()

        inserted_count = 0
        skipped_count = 0

        table_name = self.table

        try:
            # Iterate through the DataFrame and insert values into the table
            for index, row in df.iterrows():

                publish_date = row['Publish Date'] if not pd.isna(row['Publish Date']) else pd.to_datetime(0).date()
                # Handle NaN values in the 'Values' column
                inflation_values = row["Value"] if not pd.isna(row["Value"]) else 0

                # Check for existing entries with the same 'Country', 'Year', 'Month', and 'Value'
                select_query = f"""
                                SELECT COUNT(*) FROM {table_name}
                                WHERE Country = '{row['Country']}' AND Year = '{row['Year']}'
                                AND Month = '{row["Month"]}'
                                """
                cursor.execute(select_query)
                count = cursor.fetchone()[0]

                if count == 0:
                    insert_query = f"""
                             INSERT INTO {table_name} (Country, Source, UpdateFrequency, Status, Year, Month, Value, 
                             AccessDate, PublishDate, Link, Note) VALUES ( '{row['Country']}', '{row['Source']}',
                              '{row['Update frequency']}','{row['Status']}', '{row['Year']}', '{row['Month']}',
                             '{inflation_values}',NOW(), '{publish_date}', '{row['Link']}', '{row['Note']}')
                             """

                    cursor.execute(insert_query)
                    inserted_count += 1
                else:
                    skipped_count += 1

            # Commit the changes and close the connection
            mydb.commit()
            print(f"Inserted {inserted_count} records into '{table_name}' successfully.")
            if skipped_count > 0:
                print(f"Skipped {skipped_count} records as they already exist in '{table_name}'.")
        finally:
            # Always close the cursor and the connection, even in case of exceptions
            cursor.close()
            mydb.close()

    def delete_table(self, table_name=None):
        """
        Delete a MySQL table.

        Args:
            table_name (str): The name of the table to be deleted.

        """
        mydb, cursor = self.connection()

        if table_name is None:
            # If table_name is not provided, use the currently set table_name
            table_name = self.table

        try:
            # Check if the table exists
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f"Table '{table_name}' deleted successfully.")
        except conn.Error as e:
            print(f"Error deleting table '{table_name}': {str(e)}")
        finally:
            # Always close the cursor and the connection, even in case of exceptions
            cursor.close()
            mydb.close()

    def show_table(self, table_name=None):
        """
        Retrieve and display data from the current table.

        """
        mydb, cursor = self.connection()

        if table_name is None:
            # If table_name is not provided, use the currently set table_name
            table_name = self.table
        try:
            # Select all records from the table
            select_query = f"SELECT * FROM {table_name}"
            cursor.execute(select_query)

            # Fetch all records
            records = cursor.fetchall()

            # Get the column names
            column_names = [desc[0] for desc in cursor.description]

            # Display the column names
            print("Table Columns:")
            for col_name in column_names:
                print(col_name, end="\t")
            print("\n-----------------------------------")

            # Display the table data
            for row in records:
                for value in row:
                    print(value, end="\t")
                print()  # Move to the next line for the next row

        except conn.Error as e:
            print(f"Error fetching data from table '{table_name}': {str(e)}")
        finally:
            # Always close the cursor and the connection, even in case of exceptions
            cursor.close()
            mydb.close()

    @staticmethod
    def tableChoice(table_name):
        if table_name == 'Inflation':
            Indicator = 'Inflation'
            unit = 'percentage'
            title = 'Inflation rate'
            return Indicator, unit, title
        elif table_name == 'Consumer_Price_Index':
            Indicator = 'Consumer '
            unit = 'Consumer Price Index'
            title = 'Inflation rate'
            return Indicator, unit, title

    def read_database(self, table_name=None):
        if table_name is None:
            your_table = self.table
        else:
            your_table = table_name
        Indicator, unit, title = self.tableChoice(table_name)

        # Define your SQL query
        sql_query = f"SELECT * FROM {your_table}"

        # Connect to the database
        mydb, cursor = self.connection()

        # Use pandas.read_sql() to read data into a DataFrame
        df = pd.read_sql(sql_query, mydb)

        # Close the database connection
        mydb.close()

        base_col = ['No.', 'Title', 'Country', 'Source', 'Update frequency', 'Status',
                    'Year', 'Month', 'Indicator', 'Sub 1', 'Sub 2', 'Sub 3', 'Sub 4',
                    'Sub 5', 'Sub 6', 'Unit', 'Value', 'Access Date', 'Publish Date',
                    'Link', 'Note', 'Note.1']

        df.rename(columns={'No': 'No.', 'AccessDate': 'Access Date', 'PublishDate': 'Publish Date',
                           'Link': 'Link', 'UpdateFrequency': 'Update frequency'}, inplace=True)

        missing_cols = [col for col in base_col if col not in df.columns]
        unique_values = lambda x: [x]*df.shape[0]
        nrow = df.shape[0]
        for i, col in enumerate(missing_cols):
            df[col] = \
                [unique_values(title), [Indicator] * nrow, ['.'] * nrow,
                 ['.'] * nrow, ['.'] * nrow, ['.'] * nrow, ['.'] * nrow, ['.'] * nrow, [unit] * nrow, [None] * nrow][i]
            # [title, Indicator, '.', '.']
        return df[base_col]
