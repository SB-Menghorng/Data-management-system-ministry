import os

from processing.cleaning.merchandise_trad import clean_3, renameCol2Int


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

    def merchandise_trad(self):
        option = 'merchandise-trade'
        files = self.get_files(option)

        df_list = []
        for file in files:
            csv_filename = clean_3(file, self.destination_directory)
            df = renameCol2Int(csv_filename)
            df_list.append(df)

        return df_list

    def monetary_and_financial_statistics_data(self):
        option = 'monetary_and_financial_statistics_data'
        files = self.get_files(option)

        df_list = []
        for file in files:
            csv_filename = clean_3(file, self.destination_directory)
            df = renameCol2Int(csv_filename)
            df_list.append(df)

        return df_list



# path = r"D:\Intership\Labour ministry of combodain\demo"
# d = DomesticData(path)
# print(d.merchandise_trad())
# join = os.path.join(path, 'merchandise-trade')
# l = os.listdir(join)
# print(l)
# for item in l:
#     item_path = os.path.join(path, item)
#     print(item_path)
# print(os.path.join(path, 'merchandise-trade'))
