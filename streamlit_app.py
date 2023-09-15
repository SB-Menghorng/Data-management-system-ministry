from processing.visualizations.test2 import visualize_economic_data
from processing.visualizations.test import main
from processing.visualizations.merchandise_visualizing import dom_merchandise
import streamlit as st
from processing.visualizations.dashborad import dashboard1, dashboard2, dashboard3

if __name__ == "__main__":
    # Call the function to read and delete the shared data
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
        # Handle unexpected values of 'category'
        st.write("Invalid category value.")
        # Create a selectbox for menu selection
        option = st.sidebar.selectbox("Select a dashboard:", ["Dashboard 1", "Dashboard 2", "Dashboard 3"])

        # Use conditional statements to display the selected dashboard
        if option == "Dashboard 1":
            dashboard1()
        elif option == "Dashboard 2":
            main()
        elif option == "Dashboard 3":
            visualize_economic_data()
