import streamlit as st
from processing.visualizations.Inflation_Rate.Dashboard import Dashboard
from processing.visualizations.NBC import inflation_Y_on_Y
from processing.visualizations.Opec import opecdashboard

if __name__ == "__main__":

    st.set_page_config(
        page_title="Ministry of Labour and Vocational Training",
        page_icon="https://res.cloudinary.com/aquarii/image/upload/v1643955074/Ministry-of-Labour-Vocational-Training"
                  "-MoLVT-2.jpg",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.sidebar.image("https://www.minimumwage.gov.kh/wp-content/uploads/2017/11/logo_ministry_for_mobile.png")


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

    option = st.sidebar.selectbox("Select a dashboard:",
                                  ["Inflation Rate", "Contribution Inflation", "OpecBasket Price"])
    # Use conditional statements to display the selected dashboard
    if option == "Inflation Rate":
        Dashboard()

    elif option == "Contribution Inflation":
        inflation_Y_on_Y.main()
    elif option == "OpecBasket Price":
        opecdashboard.main()
