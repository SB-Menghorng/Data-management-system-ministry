import streamlit as st
import plotly.graph_objects as go
from io import BytesIO

import pandas as pd
from streamlit_option_menu import option_menu

from processing.constant import opec_file


def load_data(df):
    df = df.drop('Unnamed: 0', axis=1)
    df['data'] = pd.to_datetime(df['data'])  # Assuming 'data' is the column name for dates
    df = df.rename(columns={'data': 'Date', 'val': 'Price'})  # Rename 'data' to 'Date' and 'val' to 'Price'
    df.set_index('Date', inplace=True)
    return df


def select_data(df):
    # st.write("Select Date Range:")

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input('Start Date', value=df.index.min().date(), min_value=df.index.min().date(),
                                   max_value=df.index.max().date())
        start_date = pd.to_datetime(start_date)

    with col2:
        end_date = st.date_input('End Date', value=df.index.max().date(), min_value=df.index.min().date(),
                                 max_value=df.index.max().date())
        end_date = pd.to_datetime(end_date)

    return start_date, end_date


def get_daily_data(df, start_date, end_date):
    daily_data = df.resample('D').mean().dropna()
    daily_data = daily_data.loc[start_date:end_date]
    plot_line_graph(daily_data, start_date, end_date)


def calculate_weekly_sum(df, start_date, end_date):
    weekly_sum = df.resample('W').mean().dropna()
    weekly_sum = weekly_sum.loc[start_date:end_date]
    plot_line_graph(weekly_sum, start_date, end_date)


def get_monthly_data(df, start_date, end_date):
    df_monthly = df.resample('M').mean().dropna()
    df_monthly = df_monthly.loc[start_date:end_date]
    plot_line_graph(df_monthly, start_date, end_date)


def get_yearly_data(df, start_date, end_date):
    df_yearly = df.resample('Y').mean().dropna()
    df_yearly = df_yearly.loc[start_date:end_date]
    plot_line_graph(df_yearly, start_date, end_date)


def plot_line_graph(df, start_date=None, end_date=None):
    fig = go.Figure()

    # Filter the data based on start date and end date
    if start_date and end_date:
        df_filtered = df[(df.index >= start_date) & (df.index <= end_date)]
    elif start_date:
        df_filtered = df[df.index >= start_date]
    elif end_date:
        df_filtered = df[df.index <= end_date]
    else:
        df_filtered = df

    fig.add_trace(go.Scatter(x=df_filtered.index, y=df_filtered['Price'], mode='lines+markers',
                             marker=dict(size=5, color='steelblue'), line=dict(width=1)))
    fig.update_layout(
        xaxis=dict(
            title='Date',
            tickformat='%d-%b-%Y'  # Format for displaying date with day, month, and year
        ),
        yaxis=dict(gridcolor='lightgray'),
        plot_bgcolor='rgb(240, 240, 240)',  # Set background color
        paper_bgcolor='rgb(255, 255, 255)',  # Set paper background color

    )
    fig.update_layout(
        xaxis_title=' ',
        xaxis_title_font=dict(family='Khmer OS Siemreap', size=14, color='black')
    )
    fig.update_layout(width=900, height=450)

    col1, col2 = st.columns([5.5, 1])

    with col1:
        # Use st.expander to control the size of the graph
        with st.expander("Graph", expanded=True):
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        with st.expander("Table", expanded=True):
            # Remove the time component from the date column
            df_display = df.copy()
            df_display.index = df_display.index.date
            df_display.index.name = "Date"  # Set the index name to "Date"

            # Resize the table by setting the height parameter
            st.dataframe(df_display, use_container_width=True, height=395)

            # Add a download button for the data in Excel format
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine="xlsxwriter")
            df_display.to_excel(writer, index=True, header=True)
            writer.close()
            output.seek(0)

            with st.spinner('Downloading Excel file...'):
                st.download_button(label="Download Excel Data",
                                   data=output,
                                   file_name="data.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


def main():
    # st.markdown("""
    #     <style>
    #            .block-container {
    #                 padding-top: 0rem;
    #                 padding-bottom: 0rem;
    #                 padding-left: 12rem;
    #                 padding-right: 12rem;
    #             }
    #     </style>
    #     """, unsafe_allow_html=True)

    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.title("OPEC Basket Price")

    data_file = opec_file
    data = pd.read_csv(data_file)
    df = load_data(data)

    with st.expander("Options", expanded=True):
        selected = option_menu(
            menu_title=None,
            options=["Daily", "Weekly", "Monthly", "Yearly"],
            icons=["day", "week", "month", "year"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
        )
        start_date, end_date = select_data(df)

    if selected == "Daily":
        get_daily_data(df, start_date, end_date)
    elif selected == "Weekly":
        calculate_weekly_sum(df, start_date, end_date)
    elif selected == "Monthly":
        get_monthly_data(df, start_date, end_date)
    elif selected == "Yearly":
        get_yearly_data(df, start_date, end_date)


