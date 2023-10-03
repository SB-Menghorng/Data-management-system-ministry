from processing.cleaning.cleaner import DomesticData  # Import the DomesticData class correctly
import streamlit as st

import os


def dom_merchandise(file_directory):
    # Create an instance of the DomesticData class
    domestic_data = DomesticData(path_destination=file_directory)

    # Get the merchandise_trad data from the DomesticData class
    df_list = domestic_data.GDP()

    # List all the files in the directory (change the directory path as needed)
    file_list = os.listdir(file_directory)

    # Create a sidebar selectbox to choose a DataFrame to display
    selected_df_index = st.sidebar.selectbox("Select a DataFrame:", range(len(df_list)))

    # Display the selected DataFrame
    if selected_df_index is not None:
        selected_df = df_list[selected_df_index]
        st.write(f"Displaying content of DataFrame {selected_df_index + 1}:")

        # Display the DataFrame's content
        st.dataframe(selected_df)

# Usage example:
# file_directory = '/path/to/your/files'  # Replace with your actual directory path
# dom_merchandise(file_directory)
