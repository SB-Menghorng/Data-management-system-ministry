import pandas as pd
from pandas_profiling import ProfileReport
import streamlit.components.v1 as components

from processing.visualizations.test2 import visualize_economic_data
from processing.visualizations.test import main
from processing.visualizations.merchandise_visualizing import dom_merchandise
import streamlit as st
from processing.visualizations.dashborad import dashboard1
from processing.visualizations.Inflation_Rate.Dashboard import Dashboard

if __name__ == "__main__":

    # read_and_delete_shared_data()
    query_params = st.experimental_get_query_params()
    category = query_params.get("category", [None])[0]
    path = query_params.get("path", [""])[0]
    choice = query_params.get("choice", [""])[0]
    shared_data = {
        'category': category,
        'path': path,
        'choice': choice
    }

    if category == 'domestic':
        dom_merchandise(path)
    elif category == 'international':
        st.write('international')
        option = st.sidebar.selectbox("Select a dashboard:", ["Dashboard 1", "Dashboard 2", "Dashboard 3"])

        # Use conditional statements to display the selected dashboard
        if option == "Dashboard 1":
            dashboard1()
        elif option == "Dashboard 2":
            main()
        elif option == "Dashboard 3":
            visualize_economic_data()
    else:
        # # Handle unexpected values of 'category'
        # st.write("Invalid category value.")
        # Create a select for menu selection
        option = st.sidebar.selectbox("Select a dashboard:", ["Dashboard 1", "Dashboard 2", "Dashboard 3"])
        st.title("Pandas Profiling in Streamlit")

        # Use conditional statements to display the selected dashboard
        if option == "Dashboard 1":

            # Streamlit app title
            st.title("File Uploader and Profile Report Generator")

            # File upload widget
            uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

            # Check if a file has been uploaded
            if uploaded_file is not None:
                # Read the uploaded file into a Pandas DataFrame
                df = pd.read_csv(uploaded_file)

                # Display the first few rows of the uploaded DataFrame
                st.subheader("Preview of the uploaded data:")
                st.write(df.head())

                # Generate a profile report for the uploaded data
                st.subheader("Data Profile Report:")

                # Create a profile report
                profile = ProfileReport(df, explorative=True, progress_bar=False)

                # Display the report using Streamline's st.components
                components.html(profile.to_html(), width=800, height=600, scrolling=True)

            # Provide instructions to the user
            st.write("Please upload a CSV file to generate a data profile report.")

        elif option == "Dashboard 2":
            Dashboard()
        elif option == "Dashboard 3":
            visualize_economic_data()
