from processing.visualizations.test2 import visualize_economic_data
from processing.visualizations.test import main
from processing.visualizations.merchandise_visualizing import dom_merchandise
import streamlit as st
from processing.visualizations.dashborad import dashboard1
from processing.visualizations.Inflation_Rate.Dashboard import Dashboard

if __name__ == "__main__":
    st.set_page_config(
        page_title="Ministry of Labour and Vocational Training",
        page_icon="https://res.cloudinary.com/aquarii/image/upload/v1643955074/Ministry-of-Labour-Vocational-Training-MoLVT-2.jpg",
        layout="wide",
        initial_sidebar_state="collapsed"
        #     menu_items={
        #         'Get Help': 'https://www.extremelycoolapp.com/help',
        #         'Report a bug': 'https://www.extremelycoolapp.com/bug',
        #         'About' :"This is a header. This is an *extremely* cool app!"
        # }

    )

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

    # if category == 'domestic':
    #     dom_merchandise(path)
    # elif category == 'international':
    #     st.write('international')
    #     option = st.sidebar.selectbox("Select a dashboard:", ["Dashboard 1", "Dashboard 2"])
    #
    #     # Use conditional statements to display the selected dashboard
    #     if option == "Dashboard 1":
    #         dashboard1()
    #     elif option == "Dashboard 2":
    #         main()
    #     # elif option == "Dashboard 3":
    #         # visualize_economic_data()
    # else:
    # # Handle unexpected values of 'category'
    # st.write("Invalid category value.")
    # Create a select for menu selection
    option = st.sidebar.selectbox("Select a dashboard:", ["Inflation Rate", "Dashboard 2"])
    # Use conditional statements to display the selected dashboard
    if option == "Inflation Rate":
        Dashboard()

    elif option == "Dashboard 2":
        Dashboard()
    # elif option == "Dashboard 3":pass
