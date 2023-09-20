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

    def create_database(self, database_name):
        """
        Create a new MySQL database if it doesn't exist.

        Args:
            database_name (str): The name of the database to be created.

        """
        mydb, cursor = self.connection()

        self.database = database_name

        # Check if the database exists
        cursor.execute("SHOW DATABASES LIKE %s", (database_name))
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

    def create_table(self, table_name):
        """
        Create a MySQL table if it doesn't exist.

        Args:
            table_name (str): The name of the table to create.

        """
        mydb, cursor = self.connection()

        self.table = table_name

        # Define the SQL statement to create a table if it doesn't exist
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            No INT AUTO_INCREMENT PRIMARY KEY,
            Country VARCHAR(255),
            Status VARCHAR(255),
            Year INT,
            Month VARCHAR(255),
            Value FLOAT,
            AccessDate DATETIME,
            PublishDate DATE,
            Link VARCHAR(255),
            Note FLOAT
        )
        """
        # Execute the SQL statement to create the table
        cursor.execute(create_table_query)
        print(f"Table '{table_name}' created successfully or already exists.")

        # Don't forget to commit the changes and close the connection when you're done
        mydb.commit()
        cursor.close()
        mydb.close()

    def insert_data(self, df, InflationRate, TimePeriod, Country, Status, PublishDate, links, note_value):
        """
        Insert data from a DataFrame into a MySQL table.

        Args:
            df (pandas.DataFrame): The DataFrame containing the data to be inserted.
            InflationRate (str): The column name for the inflation rate in the DataFrame.
            TimePeriod (str): The column name for the time period in the DataFrame.
            Country (str): The column name for the country in the DataFrame.
            Status (str): The column name for the status in the DataFrame.
            PublishDate (str): The column name for the publish date in the DataFrame.
            links (str): The column name for the links in the DataFrame.

        """
        mydb, cursor = self.connection()

        inserted_count = 0
        skipped_count = 0

        table_name = self.table

        try:
            # Iterate through the DataFrame and insert values into the table
            for index, row in df.iterrows():
                # Handle NaN values in the 'Values' column
                infaltion_values = row[InflationRate] if not pd.isna(row[InflationRate]) else 0

                # Check for existing entries with the same 'Country', 'Year', 'Month', and 'Value'
                select_query = f"""
                SELECT COUNT(*) FROM {table_name}
                WHERE Country = '{Country}' AND Year = {row[TimePeriod].year}
                AND Month = '{row[TimePeriod].month}'
                """
                cursor.execute(select_query)
                count = cursor.fetchone()[0]

                if count == 0:
                    insert_query = f"""
                    INSERT INTO {table_name} (Country, Status, Year, Month, Value, AccessDate, PublishDate, Link, Note)
                    VALUES ('{Country}', '{Status}', {row[TimePeriod].year}, '{row[TimePeriod].month}',
                            {infaltion_values}, NOW(), '{PublishDate}', '{links}', {note_value})
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

