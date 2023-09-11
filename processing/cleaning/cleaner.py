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

        # Initialize a list to store the file names
        file_names = []

        # Iterate through the list to filter out files (excluding directories)
        for item in files_and_directories:
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                file_names.append(item)

        # Return the list of file names
        return file_names

    def machandis_trad(self):
        option = 'merchandise-trade'
        files = self.get_files(option)

        for file in files:
            csv_filename = clean_3(file)
            df = renameCol2Int(csv_filename)
            df


