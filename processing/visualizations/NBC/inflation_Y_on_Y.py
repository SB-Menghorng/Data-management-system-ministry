import pandas as pd
import streamlit as st
import calendar
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from io import BytesIO
import datetime
from processing.cleaning.NBC.NBC_Clean import NBC_14
from processing.constant import excelName2


def load_dataset(df):
    df = df.drop(columns=[df.columns[1]])

    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df


def select_date_range(df):
    st.sidebar.subheader("Select Date")
    # Start month and year
    start_month = st.sidebar.selectbox("Start Month", list(calendar.month_name)[1:], key="start_month_select")
    start_year = st.sidebar.selectbox("Start Year", range(df.index.year.min(), df.index.year.max() + 1),
                                      key="start_year_select")

    # End month and year
    end_month = st.sidebar.selectbox("End Month", list(calendar.month_name)[1:], key="end_month_select")
    end_year = st.sidebar.selectbox("End Year", range(df.index.year.min(), df.index.year.max() + 1),
                                    key="end_year_select")

    # Convert start and end month/year to string format
    start_month_number = list(calendar.month_name).index(start_month)
    end_month_number = list(calendar.month_name).index(end_month)
    start_date_str = f"{start_year}-{start_month_number:02d}-01"
    end_date_str = f"{end_year}-{end_month_number:02d}-01"

    # Filter data based on selected date range
    filtered_df = df.loc[start_date_str:end_date_str]

    return filtered_df


def process_selected_data(df, selected_columns):
    # Create a new DataFrame with the selected columns
    selected_df = df[selected_columns].copy()

    # Create a new column for the sum of non-selected columns
    remaining_columns = [col for col in df.columns if col not in selected_columns]
    selected_df['Other'] = df[remaining_columns].sum(axis=1)

    # Group the DataFrame by date and aggregate the columns using 'first' and 'sum' functions
    selected_df = selected_df.groupby(selected_df.index).agg(
        {**{col: 'first' for col in selected_columns}, 'Other': 'sum'})

    return selected_df


def plot_line_chart(df):
    fig = go.Figure()

    for column in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines+markers', name=column))

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
    with st.expander("Graph", expanded=True):
        st.plotly_chart(fig, use_container_width=True)


def plot_bar_chart(df):
    fig = go.Figure()

    for column in df.columns:
        fig.add_trace(go.Bar(x=df.index, y=df[column], name=column))

    fig.update_layout(
        xaxis=dict(
            title='Date',
            tickformat='%d-%b-%Y'  # Format for displaying date with day, month, and year
        ),
        yaxis=dict(gridcolor='lightgray'),
        plot_bgcolor='rgb(240, 240, 240)',  # Set background color
        paper_bgcolor='rgb(255, 255, 255)',  # Set paper background color

    )
    # fig.update_layout(
    #     xaxis_title=' ',
    #     xaxis_title_font=dict(family='Khmer OS Siemreap', size=14, color='black')
    # )
    fig.update_layout(width=900, height=450)

    with st.expander("Graph", expanded=True):
        st.plotly_chart(fig, use_container_width=True)


def show_dashBoard(df1):
    df = load_dataset(df1)

    filtered_df = select_date_range(df)

    data_names = list(filtered_df.columns)
    st.sidebar.subheader("Select Category")
    selected_columns = st.sidebar.multiselect("Select Products", data_names)
    new_df = process_selected_data(filtered_df, selected_columns)

    plot_line_chart(new_df)
    plot_bar_chart(new_df)


# Main Streamlit app
def main():
    # st.set_page_config(
    #     page_title="Ministry of Labour and Vocational Training",
    #     page_icon="https://res.cloudinary.com/aquarii/image/upload/v1643955074/Ministry-of-Labour-Vocational-Training-MoLVT-2.jpg",
    #     layout="wide",
    #
    # )

    st.markdown(
        """
        <div style="display: flex; align-items: center;margin-bottom: 30px;">
            <img src="https://cdn-icons-png.flaticon.com/128/6111/6111595.png" alt="logo" style="width: 80px; margin-right: 15px;">
            <h2 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; margin-top: 0;color: black;">Contribution Inflation</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("Options", expanded=True):
        selected = option_menu(
            menu_title=None,
            options=["Month on Month", "Year on Year"],
            icons=["month", "year"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
        )

    df1, df2 = NBC_14(excelName2)  # df1=MoM, df2 = YoY

    if not selected:
        df = load_dataset(df1)

        # Set specific start and end dates
        selected_start_date = datetime.datetime(2022, 1, 1)
        selected_end_date = datetime.datetime(2022, 12, 31)

        # Filter the DataFrame based on the specific date range
        filtered_df = df.loc[(df['Date'] >= selected_start_date) & (df['Date'] <= selected_end_date)]

        data_names = list(filtered_df.columns)
        selected_columns = ['Food and Non-Alcoholic Beverages', 'Alcoholic Beverages, Tobacco and Narcotics',
                            'Clothing and Footwear']
        new_df = process_selected_data(filtered_df, selected_columns)
        plot_line_chart(new_df)
        plot_bar_chart(new_df)

    elif selected == "Year on Year":
        show_dashBoard(df2)

    elif selected == "Month on Month":
        show_dashBoard(df1)


if __name__ == "__main__":
    main()
