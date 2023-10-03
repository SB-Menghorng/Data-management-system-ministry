import os

import pandas as pd

from processing.cleaning.GDP.merchandise_trad import clean_3, renameCol2Int
from processing.cleaning.NBC.NBC_Clean import NBC_14


class DomesticData:
    def __init__(self, path_destination):
        self.destination_directory = path_destination

    def get_files(self, options):
        # Specify the directory path you want to list files from
        directory_path = os.path.join(self.destination_directory, options)

        # Get a list of all files and directories in the specified directory
        files_and_directories = os.listdir(directory_path)

        # Initialize a list to store the file names of Excel files
        excel_files = []

        # Iterate through the list to filter out Excel files (excluding directories)
        for item in files_and_directories:
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path) and (item.endswith('.xls') or item.endswith('.xlsx')):
                excel_files.append(item_path)

        # Return the list of Excel file names
        return excel_files

    def GDP(self):
        option = 'merchandise-trade'
        files = self.get_files(option)

        df_list = []
        for file in files:
            csv_filename = clean_3(file, self.destination_directory)
            df = renameCol2Int(csv_filename)
            df_list.append(df)

        return df_list

    def NBC(self):
        option = 'monetary_and_financial_statistics_data'
        files = self.get_files(option)
        df1, df2 = None, None
        for file in files:
            if file[:26] == "14.contributiontoinflation":
                df1, df2 = NBC_14(file)
        return df1, df2
