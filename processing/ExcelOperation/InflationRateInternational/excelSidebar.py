import datetime
import calendar

import pandas as pd
import streamlit as st


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


def is_valid_month_abbreviation(abbreviation):
    return abbreviation.capitalize() in calendar.month_abbr[1:]


def timestamp_check(df, countries):
    # Assuming 'df' is your DataFrame with 'Year' and 'Month' columns
    valid_month_abbreviations = list(calendar.month_abbr)[1:]
    valid_month_full_names = list(calendar.month_name)[1:]
    month_mapping = dict(zip(valid_month_abbreviations, valid_month_full_names))

    # Function to map month abbreviations and handle non-standard values
    def map_month(month):
        if is_valid_month_abbreviation(month):
            try:
                return month_mapping.get(month.capitalize(), 'UnknownMonth')
            except AttributeError:
                return 'UnknownMonth'

    # Apply the month mapping function to the 'Month' column
    df['Month'] = df['Month'].apply(map_month)
    df = df[df['Month'] != 'UnknownMonth']

    # Create the 'YearMonth' column by combining 'Year' and transformed 'Month' columns
    try:
        df['YearMonth'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'], format='%Y-%B')
    except ValueError as e:
        print(f"Error: {e}")
        problematic_values = df.loc[df['YearMonth'].isnull(), ['Year', 'Month']]
        print("Problematic values:")
        print(problematic_values)

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
