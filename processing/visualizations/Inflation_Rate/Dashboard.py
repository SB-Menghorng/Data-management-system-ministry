import base64
import datetime
import io
import re

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from processing.constant import Inflation


def plot_line_chart(data, start_date, end_date):
    fig = go.Figure()
    selected_countries = data["Country"]
    data_columns = list(data.columns[0:])  # Convert Index object to a list

    # Convert start_date and end_date to match the data format ("%B-%Y")
    start_date_str = start_date.strftime("%B-%Y")
    end_date_str = end_date.strftime("%B-%Y")

    # Check if start_date and end_date are in data_columns
    if start_date_str not in data_columns:
        raise ValueError(f"Start date {start_date_str} is not available in the dataset.")
    if end_date_str not in data_columns:
        raise ValueError(f"End date {end_date_str} is not available in the dataset.")

    # Filter data based on start_date and end_date
    start_index = data_columns.index(start_date_str)
    end_index = data_columns.index(end_date_str) + 1
    filtered_data_columns = data_columns[start_index:end_index]

    for i, country in enumerate(selected_countries):
        values = data.loc[data['Country'] == country].iloc[:, start_index:end_index].values.flatten()
        fig.add_trace(go.Scatter(x=filtered_data_columns, y=values, mode='lines+markers', name=country))

    fig.update_layout(
        xaxis_title='កាលបរិច្ឆេទ',
        yaxis_title='អត្រាអតិផរណារ',
        xaxis_title_font=dict(family='Khmer OS Siemreap', size=14, color='black'),
        yaxis_title_font=dict(family='Khmer OS Siemreap', size=14, color='black'),
        # yaxis_tickformat='%'
    )

    fig.update_layout(width=700, height=500, showlegend=True)
    st.plotly_chart(fig)


def plot_bar_chart(data, start_date, end_date):
    fig = go.Figure()
    selected_countries = data["Country"]
    data_columns = list(data.columns[0:])  # Convert Index object to a list

    # Convert start_date and end_date to match the data format ("%B-%Y")
    start_date_str = start_date.strftime("%B-%Y")
    end_date_str = end_date.strftime("%B-%Y")

    # Check if start_date and end_date are in data_columns
    if start_date_str not in data_columns:
        raise ValueError(f"Start date {start_date_str} is not available in the dataset.")
    if end_date_str not in data_columns:
        raise ValueError(f"End date {end_date_str} is not available in the dataset.")

    # Filter data based on start_date and end_date
    start_index = data_columns.index(start_date_str)
    end_index = data_columns.index(end_date_str) + 1
    filtered_data_columns = data_columns[start_index:end_index]

    for i, country in enumerate(selected_countries):
        values = data.loc[data['Country'] == country].iloc[:, start_index:end_index].values.flatten()
        fig.add_trace(go.Bar(x=filtered_data_columns, y=values, name=country))

    fig.update_layout(
        xaxis_title='កាលបរិច្ឆេទ',
        yaxis_title='អត្រាអតិផរណារ',
        xaxis_title_font=dict(family='Khmer OS Siemreap', size=14, color='black'),
        yaxis_title_font=dict(family='Khmer OS Siemreap', size=14, color='black')
    )
    fig.update_layout(width=700, height=500, showlegend=True)
    st.plotly_chart(fig)


def load_data(df):
    df = df[['Year', 'Month', 'Country', 'Value']]
    df = df.rename(columns={'Country': 'Country', 'Year': 'Year', 'Month': 'Month', 'Value': 'Inflation Rate'})
    df['Month_Year'] = df['Month'].astype(str) + '-' + df['Year'].astype(str)

    # Create a new table with 'Month_Year' as the column and countries as rows
    new_table = df.pivot_table(index='Country', columns='Month_Year', values='Inflation Rate', aggfunc='sum')
    new_table = new_table.reset_index()

    # Reorder the columns to run from the first month of the year
    column_order = ['Country'] + sorted(new_table.columns[1:], key=lambda x: pd.to_datetime(x, format='%B-%Y'))
    new_table = new_table[column_order]

    return new_table


def pivot_table(df, start_date, end_date):
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'], format='%Y-%B')

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    pivot_table = filtered_df.pivot(index='Country', columns='Date', values='Value')

    # Format the date columns
    pivot_table.columns = pivot_table.columns.strftime('%Y-%b')

    return pivot_table


def date_input_sidebar(start_date, end_date):
    st.sidebar.subheader('Date Selection')

    start_year, start_month = start_date.year, start_date.month
    end_year, end_month = end_date.year, end_date.month

    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    selected_start_year = st.sidebar.selectbox('Start Year', range(start_year, end_year + 1), index=0)
    selected_start_month = st.sidebar.selectbox('Start Month', month_names, index=start_month - 1)

    # Get the index of the selected start month
    selected_start_month_index = month_names.index(selected_start_month)

    # Adjust the range of options for the end year based on the selected start year
    end_year_options = range(selected_start_year, end_year + 1)

    selected_end_year = st.sidebar.selectbox('End Year', end_year_options, index=len(end_year_options) - 1)

    # Calculate the index for the end year
    selected_end_year_index = selected_end_year - selected_start_year

    if selected_end_year_index == 0:
        end_month_options = month_names[selected_start_month_index:]
    elif selected_end_year_index == len(end_year_options) - 1:
        end_month_options = month_names[:end_month + 1]
    else:
        end_month_options = month_names[selected_start_month_index:]

    selected_end_month = st.sidebar.selectbox('End Month', end_month_options)

    # Get the month index and add 1 to convert it back to the month number
    selected_start_month = month_names.index(selected_start_month) + 1
    selected_end_month = month_names.index(selected_end_month) + 1

    # Construct datetime objects from the selected components
    selected_start_date = datetime.datetime(selected_start_year, selected_start_month, 1)
    selected_end_date = datetime.datetime(selected_end_year, selected_end_month, 1)

    return selected_start_date, selected_end_date


def timestamp_check(df, countries):
    df['YearMonth'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'], format='%Y-%B')

    lowest_start_date = None
    lowest_end_date = None
    lowest_duration = pd.Timedelta.max

    for country in countries:
        country_df = df[df['Country'] == country]
        min_timestamp = country_df['YearMonth'].min()
        max_timestamp = country_df['YearMonth'].max()
        timestamp_diff = max_timestamp - min_timestamp

        if timestamp_diff < lowest_duration:
            lowest_start_date = min_timestamp.date()
            lowest_end_date = max_timestamp.date()
            lowest_duration = timestamp_diff

    return lowest_start_date, lowest_end_date


def download_pivot_table_excel(pivot_table):
    # Convert the pivot table to a DataFrame
    df = pd.DataFrame(pivot_table.to_records())

    # Convert DataFrame to Excel
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine="xlsxwriter")
    excel_buffer.seek(0)

    # Encode the Excel data using base64
    b64 = base64.b64encode(excel_buffer.read()).decode()

    # Create a button with a download icon for Excel
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="pivot_table.xlsx" class="btn btn-primary">Download Excel file <i class="fa fa-download"></i></a>'

    # Add some CSS styles to make the button look beautiful
    style = """
    .btn {
        display: inline-block;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        text-decoration: none;
        background-color: #F08080;
        color:   #FF0000;
        font-size: 14px;
        margin: 4px 2px;
        cursor: pointer;
    }

    .btn-primary {
        background-color:rgb(161, 219, 255, 0.3);
    }

    .btn-primary:hover {
        background-color:#191970;
    }

    .fa-download {
        margin-left: 5px;
    }
    .download-container {
        display: flex;
        justify-content: left;
        margin-top:-30px;
        margin-bottom:15px;
    }
    """
    st.markdown(f'<style>{style}</style>', unsafe_allow_html=True)
    st.markdown(f'<div class="download-container">{href}</div>', unsafe_allow_html=True)


def find_countries_with_cpli_or_base(df, selected_start_date, selected_end_date, selected_countries=None):
    country_notes = []

    filtered_df = df[(df['Year'] >= selected_start_date.year) & (df['Year'] <= selected_end_date.year)]

    filtered_df = filtered_df.drop_duplicates(subset=['Country', 'Note'])

    for _, row in filtered_df.iterrows():
        year = row['Year']
        note = row['Note']

        if re.search(r'(CPI|Base|base)\s+(\d{4})', str(note), re.IGNORECASE):
            country = row['Country']

            if selected_countries is not None and country not in selected_countries:
                continue

            country_notes.append({'year': year, 'country': country, 'note': note})

    for item in country_notes:
        st.write("Note: "f"{item['country']} {item['note']}")

    return country_notes


def category_data(df, start_date, end_date):
    start_date = pd.to_datetime(start_date, format='%Y-%m')
    end_date = pd.to_datetime(end_date, format='%Y-%m')
    filtered_df = df[(df['YearMonth'] >= start_date) & (df['YearMonth'] <= end_date)]

    max_row = filtered_df[filtered_df["Value"] == filtered_df["Value"].max()]
    min_row = filtered_df[filtered_df["Value"] == filtered_df["Value"].min()]
    avg_value = filtered_df["Value"].mean()
    update_frequency = filtered_df["Update frequency"].iloc[0]

    return max_row, min_row, avg_value, update_frequency


def business_partners(df):
    bpc = ["China", "European Union 27", "Japan", "United States"]
    bp_df = df[df["Country"].isin(bpc)]

    # Side Bar
    country = st.sidebar.multiselect("Select Countries", bp_df["Country"].unique(), key="business_countries")
    if country:
        filtered_df = bp_df[bp_df["Country"].isin(country)]
        lowest_start_date, lowest_end_date = timestamp_check(filtered_df, country)
        selected_start_date, selected_end_date = date_input_sidebar(lowest_start_date, lowest_end_date)
        st.markdown(
            """
            <div style="display: flex; align-items: center;">
                <img src="https://symbolshub.org/wp-content/uploads/2019/10/bullet-point-symbol.png" alt="logo" style="width: 25px; margin-right: 5px; vertical-align: middle;">
                <h3 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; margin-top: 0; font-size: 18px; font-weight: bold; vertical-align: middle;">តារាងទិន្នន័យនៃប្រទេសដែលជាដៃគូពាណិជ្ជកម្ម</h3><br><br><br>
            </div>
            """,
            unsafe_allow_html=True
        )
        result = pivot_table(filtered_df, selected_start_date, selected_end_date)
        result_styled = result.style.set_properties(**{'background-color': 'rgb(161, 219, 255, 0.3)', 'color': 'black'})
        st.dataframe(result_styled)
        download_pivot_table_excel(result)
        st.markdown(
            """
            <div style="display: flex; align-items: center;">
                <img src="https://symbolshub.org/wp-content/uploads/2019/10/bullet-point-symbol.png" alt="logo" style="width: 25px; margin-right: 5px; vertical-align: middle;">
                <h3 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; margin-top: 0; font-size: 18px; font-weight: bold; vertical-align: middle;">អត្រាអតិផរណារបស់ប្រទេសដៃគូប្រកួតប្រជែង</h3><br><br><br>
            </div>
            """,
            unsafe_allow_html=True
        )
        new_table = load_data(filtered_df)
        max_row, min_row, avg_value, update_frequency = category_data(filtered_df, selected_start_date,
                                                                      selected_end_date)
        col1, col2, col3, col4 = st.columns(4)

        box_color = "rgba(161, 219, 255, 0.3)"
        border_color = "#87CEFA"

        with col1:
            st.markdown(
                f'<div style="background-color: {box_color}; padding: 10px; border-radius: 5px;">'
                f'<img src="https://cdn-icons-png.flaticon.com/512/5198/5198491.png" style="width: 25px; height: 25px; margin-right: 10px;">'
                f'<span style="color: black; font-weight: bold;">Maximum Inflation Rate</span></div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div style="border: 2px solid {border_color}; padding: 10px; border-radius: 5px; margin-top: 10px;">'
                f'<span style="font-size: 18px;">{max_row["Country"].values[0]}</span>: <br>'
                f'<span style="font-size: 24px;">{max_row["Value"].values[0]}</span></div>',
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f'<div style="background-color: {box_color}; padding: 10px; border-radius: 5px;">'
                f'<img src="https://cdn1.iconfinder.com/data/icons/vibrancie-action/30/action_059-trending_down-arrow-up-decrease-512.png" style="width: 25px; height: 25px; margin-right: 10px;">'
                f'<span style="color: black; font-weight: bold;">Minimum Inflation Rate</span></div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div style="border: 2px solid {border_color}; padding: 10px; border-radius: 5px; margin-top: 10px;">'
                f'<span style="font-size: 18px;">{min_row["Country"].values[0]}</span>: <br>'
                f'<span style="font-size: 24px;">{min_row["Value"].values[0]}</span></div>',
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f'<div style="background-color: {box_color}; padding: 10px; border-radius: 5px;">'
                f'<img src="https://cdn-icons-png.flaticon.com/512/5360/5360536.png" style="width: 25px; height: 25px; margin-right: 10px;">'
                f'<span style="color: black; font-weight: bold;">Average Inflation Rate</span></div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div style="border: 2px solid {border_color}; padding: 10px; border-radius: 5px; margin-top: 10px;">'
                f'<span style="font-size: 18px;">{"Average Rate"}</span>: <br>'
                f'<span style="font-size: 24px;">{avg_value}</span></div>',
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                f'<div style="background-color: {box_color}; padding: 10px; border-radius: 5px;">'
                f'<img src="https://cdn-icons-png.flaticon.com/512/2546/2546705.png" style="width: 25px; height: 25px; margin-right: 10px;">'
                f'<span style="color: black; font-weight: bold;">Update Frequency</span></div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div style="border: 2px solid {border_color}; padding: 10px; border-radius: 5px; margin-top: 10px;">'
                f'<span style="font-size: 18px;">{"Update"}</span>: <br>'
                f'<span style="font-size: 24px;">{update_frequency}</span></div>',
                unsafe_allow_html=True
            )

        column_width = "50%"
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div style="width: {700};"></div>', unsafe_allow_html=True)
            plot_line_chart(new_table, selected_start_date, selected_end_date)
        with col2:
            st.markdown(f'<div style="width: {400};"></div>', unsafe_allow_html=True)
            plot_bar_chart(new_table, selected_start_date, selected_end_date)
        country_notes = find_countries_with_cpli_or_base(df, selected_start_date, selected_end_date, country)
        # st.write(country_notes)


def competitors(df):
    # comp=compititors
    comp_countries = ["Bangladesh", "Indonesia ", "Thailand", "Vietnam", "Sri Lanka", "Philipinas", "Malaysia", "Lao",
                      "Singapore"]
    comp_df = df[df["Country"].isin(comp_countries)]
    # st.table(comp_df, 100, 200)

    # Side Bar
    country = st.sidebar.multiselect("Select Countries", comp_df["Country"].unique(), key="competitor_countries")
    if country:
        filtered_df = comp_df[comp_df["Country"].isin(country)]
        lowest_start_date, lowest_end_date = timestamp_check(filtered_df, country)
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
        result = pivot_table(filtered_df, selected_start_date, selected_end_date)
        result_styled = result.style.set_properties(**{'background-color': 'rgb(161, 219, 255, 0.3)', 'color': 'black'})
        st.dataframe(result_styled)
        download_pivot_table_excel(result)
        st.markdown(
            """
            <div style="display: flex; align-items: center;">
                <img src="https://symbolshub.org/wp-content/uploads/2019/10/bullet-point-symbol.png" alt="logo" style="width: 25px; margin-right: 5px; vertical-align: middle;">
                <h3 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; margin-top: 0; font-size: 18px; font-weight: bold; vertical-align: middle;">អត្រាអតិផរណារបស់ប្រទេសដៃគូប្រកួតប្រជែង</h3><br><br><br>
            </div>
            """,
            unsafe_allow_html=True
        )
        new_table = load_data(filtered_df)
        max_row, min_row, avg_value, update_frequency = category_data(filtered_df, selected_start_date,
                                                                      selected_end_date)
        col1, col2, col3, col4 = st.columns(4)

        box_color = "rgba(161, 219, 255, 0.3)"
        border_color = "#87CEFA"

        with col1:
            st.markdown(
                f'<div style="background-color: {box_color}; padding: 10px; border-radius: 5px;">'
                f'<img src="https://cdn-icons-png.flaticon.com/512/5198/5198491.png" style="width: 25px; height: 25px; margin-right: 10px;">'
                f'<span style="color: black; font-weight: bold;">Maximum Inflation Rate</span></div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div style="border: 2px solid {border_color}; padding: 10px; border-radius: 5px; margin-top: 10px;">'
                f'<span style="font-size: 18px;">{max_row["Country"].values[0]}</span>: <br>'
                f'<span style="font-size: 24px;">{max_row["Value"].values[0]}</span></div>',
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f'<div style="background-color: {box_color}; padding: 10px; border-radius: 5px;">'
                f'<img src="https://cdn1.iconfinder.com/data/icons/vibrancie-action/30/action_059-trending_down-arrow-up-decrease-512.png" style="width: 25px; height: 25px; margin-right: 10px;">'
                f'<span style="color: black; font-weight: bold;">Minimum Inflation Rate</span></div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div style="border: 2px solid {border_color}; padding: 10px; border-radius: 5px; margin-top: 10px;">'
                f'<span style="font-size: 18px;">{min_row["Country"].values[0]}</span>: <br>'
                f'<span style="font-size: 24px;">{min_row["Value"].values[0]}</span></div>',
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f'<div style="background-color: {box_color}; padding: 10px; border-radius: 5px;">'
                f'<img src="https://cdn-icons-png.flaticon.com/512/5360/5360536.png" style="width: 25px; height: 25px; margin-right: 10px;">'
                f'<span style="color: black; font-weight: bold;">Average Inflation Rate</span></div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div style="border: 2px solid {border_color}; padding: 10px; border-radius: 5px; margin-top: 10px;">'
                f'<span style="font-size: 18px;">{"Average Rate"}</span>: <br>'
                f'<span style="font-size: 24px;">{avg_value}</span></div>',
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                f'<div style="background-color: {box_color}; padding: 10px; border-radius: 5px;">'
                f'<img src="https://cdn-icons-png.flaticon.com/512/2546/2546705.png" style="width: 25px; height: 25px; margin-right: 10px;">'
                f'<span style="color: black; font-weight: bold;">Update Frequency</span></div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div style="border: 2px solid {border_color}; padding: 10px; border-radius: 5px; margin-top: 10px;">'
                f'<span style="font-size: 18px;">{"Update"}</span>: <br>'
                f'<span style="font-size: 24px;">{update_frequency}</span></div>',
                unsafe_allow_html=True
            )

        # st.dataframe(new_table)
        column_width = "50%"
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div style="width: {700};"></div>', unsafe_allow_html=True)
            plot_line_chart(new_table, selected_start_date, selected_end_date)
        with col2:
            st.markdown(f'<div style="width: {400};"></div>', unsafe_allow_html=True)
            plot_bar_chart(new_table, selected_start_date, selected_end_date)
        country_notes = find_countries_with_cpli_or_base(df, selected_start_date, selected_end_date, country)
        # st.write(country_notes)


def default_mode(df):
    # comp=compititors
    def_countries = ["Bangladesh", "Indonesia ", "Thailand", "Vietnam", "Singapore"]
    def_df = df[df["Country"].isin(def_countries)]
    # st.table(comp_df, 100, 200)

    selected_start_date, selected_end_date = timestamp_check(def_df, def_countries)
    st.markdown(
        """
        <div style="display: flex; align-items: center;">
            <img src="https://symbolshub.org/wp-content/uploads/2019/10/bullet-point-symbol.png" alt="logo" style="width: 25px; margin-right: 5px; vertical-align: middle;">
            <h3 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; margin-top: 0; font-size: 18px; font-weight: bold; vertical-align: middle;">តារាងទិន្នន័យនៃប្រទេសដែលជាដៃគូពាណិ្ចចកម្ម</h3><br><br><br>
        </div>
        """,
        unsafe_allow_html=True
    )
    result = pivot_table(def_df, selected_start_date, selected_end_date)
    result_styled = result.style.set_properties(**{'background-color': 'rgb(161, 219, 255, 0.3)', 'color': 'black'})
    st.dataframe(result_styled)
    download_pivot_table_excel(result)
    st.markdown(
        """
        <div style="display: flex; align-items: center;">
            <img src="https://symbolshub.org/wp-content/uploads/2019/10/bullet-point-symbol.png" alt="logo" style="width: 25px; margin-right: 5px; vertical-align: middle;">
            <h3 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; margin-top: 0; font-size: 18px; font-weight: bold; vertical-align: middle;">អត្រាអតិផរណារបស់ប្រទេសដៃគូប្រកួតប្រជែង</h3><br><br><br>
        </div>
        """,
        unsafe_allow_html=True
    )
    new_table = load_data(def_df)
    max_row, min_row, avg_value, update_frequency = category_data(def_df, selected_start_date, selected_end_date)
    col1, col2, col3, col4 = st.columns(4)

    box_color = "rgba(161, 219, 255, 0.3)"
    border_color = "#87CEFA"

    with col1:
        st.markdown(
            f'<div style="background-color: {box_color}; padding: 10px; border-radius: 5px;">'
            f'<img src="https://cdn-icons-png.flaticon.com/512/5198/5198491.png" style="width: 25px; height: 25px; margin-right: 10px;">'
            f'<span style="color: black; font-weight: bold;">Maximum Inflation Rate</span></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div style="border: 2px solid {border_color}; padding: 10px; border-radius: 5px; margin-top: 10px;">'
            f'<span style="font-size: 18px;">{max_row["Country"].values[0]}</span>: <br>'
            f'<span style="font-size: 24px;">{max_row["Value"].values[0]}</span></div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f'<div style="background-color: {box_color}; padding: 10px; border-radius: 5px;">'
            f'<img src="https://cdn1.iconfinder.com/data/icons/vibrancie-action/30/action_059-trending_down-arrow-up-decrease-512.png" style="width: 25px; height: 25px; margin-right: 10px;">'
            f'<span style="color: black; font-weight: bold;">Minimum Inflation Rate</span></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div style="border: 2px solid {border_color}; padding: 10px; border-radius: 5px; margin-top: 10px;">'
            f'<span style="font-size: 18px;">{min_row["Country"].values[0]}</span>: <br>'
            f'<span style="font-size: 24px;">{min_row["Value"].values[0]}</span></div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f'<div style="background-color: {box_color}; padding: 10px; border-radius: 5px;">'
            f'<img src="https://cdn-icons-png.flaticon.com/512/5360/5360536.png" style="width: 25px; height: 25px; margin-right: 10px;">'
            f'<span style="color: black; font-weight: bold;">Average Inflation Rate</span></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div style="border: 2px solid {border_color}; padding: 10px; border-radius: 5px; margin-top: 10px;">'
            f'<span style="font-size: 18px;">{"Average Rate"}</span>: <br>'
            f'<span style="font-size: 24px;">{avg_value}</span></div>',
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f'<div style="background-color: {box_color}; padding: 10px; border-radius: 5px;">'
            f'<img src="https://cdn-icons-png.flaticon.com/512/2546/2546705.png" style="width: 25px; height: 25px; margin-right: 10px;">'
            f'<span style="color: black; font-weight: bold;">Update Frequency</span></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div style="border: 2px solid {border_color}; padding: 10px; border-radius: 5px; margin-top: 10px;">'
            f'<span style="font-size: 18px;">{"Update"}</span>: <br>'
            f'<span style="font-size: 24px;">{update_frequency}</span></div>',
            unsafe_allow_html=True
        )

    # st.dataframe(new_table)
    column_width = "50%"
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div style="width: {700};"></div>', unsafe_allow_html=True)
        plot_line_chart(new_table, selected_start_date, selected_end_date)
    with col2:
        st.markdown(f'<div style="width: {400};"></div>', unsafe_allow_html=True)
        plot_bar_chart(new_table, selected_start_date, selected_end_date)

    country_notes = find_countries_with_cpli_or_base(df, selected_start_date, selected_end_date, def_countries)
    # st.write(country_notes)


def Dashboard():
    df = pd.read_csv(Inflation)

    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.markdown(
        """
        <div style="display: flex; align-items: center;">
            <img src="https://cdn3d.iconscout.com/3d/free/thumb/free-line-chart-growth-3814121-3187502.png" alt="logo" style="width: 90px; margin-right: 15px;">
            <h3 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; margin-top: 0;">ការវិភាគអត្រាអតិផរណារ</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.image("https://www.minimumwage.gov.kh/wp-content/uploads/2017/11/logo_ministry_for_mobile.png")
    options = st.sidebar.selectbox(
        'Choose Category',
        [' ', 'Business partners', 'Competitors']
    )
    # Interface design
    # Add the logo and title within a customizable box
    if options == 'Business partners':
        business_partners(df)
    elif options == 'Competitors':
        competitors(df)
    else:
        default_mode(df)


if __name__ == '__main__':
    Dashboard()
