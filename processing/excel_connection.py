import pandas as pd
from openpyxl import load_workbook


class Excel:
    """
    The `Excel` class provides methods for updating and managing existing Excel files, including row-level validation
    and deleting rows based on conditions.

    Attributes:
        excel_file (str): The path to the existing Excel file.
        sheet_name (str): The name of the sheet within the Excel file.

    Methods:
        update_excel_with_row_level_validation(self, external_data, columns_to_verify=None):
            Updates an existing Excel file with row-level validation for specified columns using external data.

        delete_rows_from_excel_multiple_conditions(self, conditions):
            Deletes rows from an existing Excel file based on multiple conditions.

    Use Case:
        The `Excel` class simplifies interactions with Excel files in Python, making it a useful tool for projects that
        involve Excel data management, import, and export.

    Example Usage:
        # Create an Excel object
        excel = Excel(excel_file='data.xlsx', sheet_name='Sheet1')

        # Update Excel with row-level validation
        external_data = pd.read_excel('new_data.xlsx')
        excel.update_excel_with_row_level_validation(external_data, columns_to_verify=['Title', 'Country', 'Indicator'])

        # Delete rows based on conditions  = [(1, 'Value1'), (2, 'Value2')]
        excel.delete_rows_from_excel_multiple_conditions(conditions)
    """
    def __init__(self, excel_file, sheet_name):
        """
        Initialize an Excel object for updating an existing Excel file.

        Parameters:
        - excel_file (str): The path to the existing Excel file.
        - sheet_name (str): The name of the sheet within the Excel file.

        Returns:
        - None
        """
        self.excel_file = excel_file
        self.sheet_name = sheet_name

    def update_excel_with_row_level_validation(self, external_data, columns_to_verify=None):
        """
        Update an existing Excel file with row-level validation for specified columns.

        Parameters:
        - external_data (pd.DataFrame): The DataFrame containing the data to append.
        - columns_to_verify (list): A list of column names to verify for duplicates.

        Returns:
        - None
        """
        if columns_to_verify is None:
            columns_to_verify = ['Title', 'Country', 'Indicator']
        excel_file, sheet_name = self.excel_file, self.sheet_name

        try:
            # Load the existing Excel file
            wb = load_workbook(excel_file)

            # Load existing data from Excel into a DataFrame
            existing_data = pd.read_excel(excel_file, sheet_name=sheet_name)

            # Calculate row numbers for 'No.' column
            n = existing_data.shape[0] + external_data.shape[0]
            no = [i for i in range(n, 0, -1)]
            no = no[:external_data.shape[0]]
            external_data['No.'] = no[::-1]

            # Find the last row number in the existing Excel sheet
            last_row = existing_data.shape[0] + 2  # Add 2 to account for the header row and 1-based indexing

            # Initialize a list to store duplicate rows
            duplicate_rows = []

            # Iterate through each row in the external data
            for index, row in external_data.iterrows():
                # Create a condition to check for duplicates in the existing data
                condition = (existing_data[columns_to_verify] == row[columns_to_verify]).all(axis=1).all()

                # If a duplicate is found, add the row to the list
                if condition:
                    duplicate_rows.append(index)

            # Check if any duplicate rows were found
            if duplicate_rows:
                print("Duplicate rows found. Update aborted.")
                wb.close()
                return

            # Calculate the starting row for appending data
            start_row = last_row

            # Append only new data to the Excel file starting from the last row
            writer = pd.ExcelWriter(excel_file, engine='openpyxl')
            writer.book = wb
            external_data.to_excel(writer, sheet_name=sheet_name, index=False, startrow=start_row, header=False)
            writer.save()
            wb.close()
            print("Excel file updated successfully.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def delete_rows_from_excel_multiple_conditions(self, conditions):
        """
        Delete rows from an existing Excel file based on multiple conditions.

        Parameters:
        - excel_file (str): The path to the existing Excel file.
        - sheet_name (str): The name of the sheet from which to delete rows.
        - conditions (list of tuples): A list of (condition_column_index, condition_value) tuples.

        Returns:
        - None
        """
        excel_file, sheet_name = self.excel_file, self.sheet_name

        try:
            # Load the existing Excel file
            wb = load_workbook(excel_file)

            # Select the worksheet
            sheet = wb[sheet_name]

            # Store the row indices to delete
            rows_to_delete = []

            conditions = list(conditions)

            # Iterate through rows to identify rows to delete
            for row_index, row in enumerate(sheet.iter_rows(min_row=0, values_only=True)):
                for condition_column, condition_value in conditions:
                    if row[condition_column] == condition_value:  # Adjust column index to 0-based
                        rows_to_delete.append(row_index + 1)

            # Delete rows in reverse order to avoid issues with row indices
            for row_index in reversed(rows_to_delete):
                sheet.delete_rows(row_index)

            # Save the modified Excel file
            wb.save(excel_file)
            wb.close()
            print("Rows deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def show_excel(self):
        return pd.read_excel(self.excel_file, sheet_name=self.sheet_name)
