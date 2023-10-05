import streamlit as st
import pandas as pd
from processing.ExcelOperation.InflationRateInternational.excelSidebar import date_input_sidebar, timestamp_check
from processing.connection.database import Database
from processing.connection.excel import Excel
from processing.constant import host, password, user, database_name, table_name1, table_name2, excelPathConst, \
    sheetNameConst


def load_data(df, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    # Format the "year" column as a string without commas
    df['Year'] = df['Year'].apply(lambda x: '{:.0f}'.format(x))
    edite_table = st.data_editor(df, num_rows="dynamic", key="data_editor")
    return edite_table


def filter_data_by_country(df, country_filter):
    if not country_filter:  # If no country is selected, display data for all countries
        filtered_df = df
    else:  # If one or more countries are selected, display data for the selected countries
        filtered_df = df[df["Country"].isin(country_filter)]
    return filtered_df


def dashboardExcel():
    st.set_page_config(
        page_title="Ministry of Labour and Vocational Training",
        page_icon="https://res.cloudinary.com/aquarii/image/upload/v1643955074/Ministry-of-Labour-Vocational-Training-MoLVT-2.jpg",
        layout="wide",

    )

    st.sidebar.image("https://www.minimumwage.gov.kh/wp-content/uploads/2017/11/logo_ministry_for_mobile.png")
    st.markdown(
        """
            <div style="display: flex; align-items: center;">
                <img src="https://cdn-icons-png.flaticon.com/128/2906/2906274.png" style="width: 50px; height: 50px; margin-right: 20px">
                <h3 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; margin-top: 0; font-size: 22px; font-weight: bold; vertical-align: middle;">តារាងទិន្នន័យដែលបានទាញមក</h3><br><br><br>
            </div>
            """,
        unsafe_allow_html=True
    )
    # Set CSS styles
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            position: sticky;
            top: 0px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    db = Database(host=host, password=password, user=user, database=database_name, table=table_name1)

    df1 = db.read_database(table_name=table_name1)
    df2 = db.read_database(table_name=table_name2)

    st.sidebar.subheader("Configure the Table")
    options = st.sidebar.selectbox(
        'Choose Category',
        ['Business Partners', 'Competitors']
    )
    if options == 'Competitors':
        comp_countries = df2["Country"].unique()
        comp_df = df2[df2["Country"].isin(comp_countries)]
        country_filter = st.sidebar.multiselect("Select Countries", comp_df["Country"].unique(),
                                                key="competitor_countries")
        filtered_df = filter_data_by_country(comp_df, country_filter)
        lowest_start_date, lowest_end_date = timestamp_check(filtered_df, comp_countries)
        selected_start_date, selected_end_date = date_input_sidebar(lowest_start_date, lowest_end_date)
        st.markdown(
            """
            <div style="display: flex; align-items: center;">
                <img src="https://symbolshub.org/wp-content/uploads/2019/10/bullet-point-symbol.png" alt="logo" style="width: 25px; margin-right: 5px; vertical-align: middle;">
                <h3 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; margin-top: 0; font-size: 18px; font-weight: bold; vertical-align: middle;">តារាងទិន្នន័យនៃប្រទេសដែលជាដៃគូពាណិ្ចចកម្ម</h3><br><br><br>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([5, 1])
        with col1:
            with st.expander("Table", expanded=True):
                result = load_data(filtered_df, selected_start_date, selected_end_date)

        with col2:
            # Define the HTML for the logo
            with st.expander("Excel Input", expanded=True):

                # Add a text input for the sheet name
                sheetName = st.text_input("Sheet Name", key="sheet_name_input")

                # Add a text input for the Excel path
                excelPath = st.text_input("Excel Path", key="excel_path_input")

                # Apply color to the input fields
                st.markdown("<style>input[type=text] { background-color: #F0F8FF; }</style>", unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col2:
                    st.write(" ")
                    # Add a button for Insert
                    button_Insert = st.button('Insert ')

                    # Check if the Insert button is clicked
                    if button_Insert:
                        if not excelPath or not sheetName:
                            excelOpt = Excel(excel_file=excelPathConst, sheet_name=sheetNameConst)
                            excelOpt.insert_into_existing_excel(result)
                        else:
                            excelOpt = Excel(excel_file=excelPath, sheet_name=sheetName)
                            excelOpt.insert_into_existing_excel(result)

                with col1:
                    logo_html_1 = """
                        <div>
                            <span>
                                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Microsoft_Office_Excel_%282019%E2%80%93present%29.svg/2203px-Microsoft_Office_Excel_%282019%E2%80%93present%29.svg.png" alt="Logo" style="width: 60px; height: 60px; margin-right: 10px; margin-left: 10px ; margin-top: 10px; margin-bottom: 20px;">
                            </span>
                        </div>
                    """
                    # Render the HTML code
                    st.markdown(logo_html_1, unsafe_allow_html=True)

            # Define the HTML for the logo
            logo_html = """
                <div>
                    <span>
                        <img src="https://seeklogo.com/images/A/amazon-database-logo-BAA099F432-seeklogo.com.png" alt="Logo" style="width: 45px; height: 50px; margin-right: 10px;margin-left: 10px; margin-top: -8px; margin-bottom: 7px">
                    </span>
                </div>
            """

            # Create the expander with customized title
            with st.expander("Database Update", expanded=True):
                st.write(" ")
                col1, col2 = st.columns(2)
                with col1:
                    # Render the HTML code
                    st.markdown(logo_html, unsafe_allow_html=True)
                    st.write(" ")
                with col2:
                    # Add a button for Update with custom CSS style
                    button_Update = st.button('Update')
                    # Check if the Update button is clicked
                    if button_Update:
                        if button_Update:
                            db.delete_table()
                            db.create_table()
                            db.insert_data(result)

        # statisticSummaryBox(filtered_df, selected_start_date, selected_end_date)

    elif options == "Business Partners":
        comp_countries = df1["Country"].unique()
        comp_df = df1[df1["Country"].isin(comp_countries)]
        country_filter = st.sidebar.multiselect("Select Countries", comp_df["Country"].unique(),
                                                key="competitor_countries")
        filtered_df = filter_data_by_country(comp_df, country_filter)
        lowest_start_date, lowest_end_date = timestamp_check(filtered_df, comp_countries)
        selected_start_date, selected_end_date = date_input_sidebar(lowest_start_date, lowest_end_date)
        st.markdown(
            """
            <div style="display: flex; align-items: center;">
                <img src="https://symbolshub.org/wp-content/uploads/2019/10/bullet-point-symbol.png" alt="logo" style="width: 25px; margin-right: 5px; vertical-align: middle;">
                <h3 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; margin-top: 0; font-size: 18px; font-weight: bold; vertical-align: middle;">តារាងទិន្នន័យនៃប្រទេសដែលជាដៃគូពាណិ្ចចកម្ម</h3><br><br><br>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([5, 1])
        with col1:
            with st.expander("Table", expanded=True):
                result = load_data(filtered_df, selected_start_date, selected_end_date)

        with col2:
            # Define the HTML for the logo
            with st.expander("Excel Input", expanded=True):

                # Add a text input for the sheet name
                sheetName = st.text_input("Sheet Name", key="sheet_name_input")

                # Add a text input for the Excel path
                excelPath = st.text_input("Excel Path", key="excel_path_input")

                # Apply color to the input fields
                st.markdown("<style>input[type=text] { background-color: #F0F8FF; }</style>", unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col2:
                    st.write(" ")
                    # Add a button for Insert
                    button_Insert = st.button('Insert ')

                    # Check if the Insert button is clicked
                    if button_Insert:
                        if not excelPath or not sheetName:
                            excelOpt = Excel(excel_file=excelPathConst, sheet_name=sheetNameConst)
                            excelOpt.insert_into_existing_excel(result)
                        else:
                            excelOpt = Excel(excel_file=excelPath, sheet_name=sheetName)
                            excelOpt.insert_into_existing_excel(result)

                with col1:
                    logo_html_1 = """
                              <div>
                                  <span>
                                      <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Microsoft_Office_Excel_%282019%E2%80%93present%29.svg/2203px-Microsoft_Office_Excel_%282019%E2%80%93present%29.svg.png" alt="Logo" style="width: 60px; height: 60px; margin-right: 10px; margin-left: 10px ; margin-top: 10px; margin-bottom: 20px;">
                                  </span>
                              </div>
                          """
                    # Render the HTML code
                    st.markdown(logo_html_1, unsafe_allow_html=True)

            # Define the HTML for the logo
            logo_html = """
                      <div>
                          <span>
                              <img src="https://seeklogo.com/images/A/amazon-database-logo-BAA099F432-seeklogo.com.png" alt="Logo" style="width: 45px; height: 50px; margin-right: 10px;margin-left: 10px; margin-top: -8px; margin-bottom: 7px">
                          </span>
                      </div>
                  """

            # Create the expander with customized title
            with st.expander("Database Update", expanded=True):
                st.write(" ")
                col1, col2 = st.columns(2)
                with col1:
                    # Render the HTML code
                    st.markdown(logo_html, unsafe_allow_html=True)
                    st.write(" ")
                with col2:
                    # Add a button for Update with custom CSS style
                    button_Update = st.button('Update')
                    # Check if the Update button is clicked
                    if button_Update:
                        if button_Update:
                            db.delete_table()
                            db.create_table()
                            db.insert_data(result)

        # statisticSummaryBox(filtered_df, selected_start_date, selected_end_date)


