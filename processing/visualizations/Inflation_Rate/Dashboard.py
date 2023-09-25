import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import datetime
import re
import base64

def plot_line_chart(data, start_date, end_date):
    fig = go.Figure()
    selected_countries = data["Country"]
    data_columns = list(data.columns[1:])  # Convert Index object to a list
    
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
    
    fig.update_layout(xaxis_title='កាលបរិច្ឆេទ', yaxis_title='អត្រាអតិផរណារ')
    fig.update_layout(width=700, height=500, showlegend=True)
    st.plotly_chart(fig)
    
def plot_bar_chart(data, start_date, end_date):
    fig = go.Figure()
    selected_countries = data["Country"]
    data_columns = list(data.columns[1:])  # Convert Index object to a list
    
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
    
    fig.update_layout(xaxis_title='កាលបរិច្ឆេទ', yaxis_title='អត្រាអតិផរណារ')
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

# def date_input_sidebar(start_date, end_date):
#     st.sidebar.subheader('Date Selection')
#     selected_start_date = st.sidebar.date_input('Start Date', start_date, min_value=start_date, max_value=end_date)
#     selected_end_date = st.sidebar.date_input('End Date', end_date, min_value=selected_start_date, max_value=end_date)
#     return selected_start_date, selected_end_date

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

    # Adjust the range of options for the end month based on the selected start month and year
    if selected_end_year_index == 0:
        end_month_options = month_names[start_month - 1:end_month]
    elif selected_end_year_index == len(end_year_options) - 1:
        end_month_options = month_names[:end_month]
    else:
        end_month_options = month_names

    selected_end_month = st.sidebar.selectbox('End Month', end_month_options, index=end_month - 1)

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

# def download_pivot_table_csv(pivot_table):
#     # Convert the pivot table to a DataFrame
#     df = pd.DataFrame(pivot_table.to_records())

#     # Prompt the user to download the CSV file
#     csv = df.to_csv(index=False)
#     b64 = base64.b64encode(csv.encode()).decode()
#     href = f'<a href="data:file/csv;base64,{b64}" download="pivot_table.csv">Download CSV file</a>'
#     st.markdown(href, unsafe_allow_html=True)  
def download_pivot_table_csv(pivot_table):
    # Convert the pivot table to a DataFrame
    df = pd.DataFrame(pivot_table.to_records())

    # Prompt the user to download the CSV file
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()

    # Create a button with a download icon
    href = f'<a href="data:file/csv;base64,{b64}" download="pivot_table.csv" class="btn btn-primary">Download CSV file <i class="fa fa-download"></i></a>'

    # Add some CSS styles to make the button look beautiful
    style = """
    .btn {
        display: inline-block;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        text-decoration: none;
        background-color: #F08080;
        color: 	#FF0000;
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
        margin-top:-5px;
        margin_button:50px;
    }
    """

 # Display the button with the CSS styles
    st.markdown(f'<style>{style}</style>', unsafe_allow_html=True)
    st.markdown(f'<div class="download-container">{href}</div>', unsafe_allow_html=True)

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
                <h3 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; margin-top: 0; font-size: 12px; font-weight: bold; vertical-align: middle;">តារាងទិន្នន័យនៃប្រទេសដែលជាដៃគូពាណិជ្ជកម្ម</h3><br><br><br>
            </div>
            """,
            unsafe_allow_html=True
        )
        result = pivot_table(filtered_df, selected_start_date, selected_end_date)
        result_styled = result.style.set_properties(**{'background-color': 'rgb(161, 219, 255, 0.3)', 'color': 'black'})
        st.dataframe(result_styled)
        download_pivot_table_csv(result)
        st.markdown(
            """
            <div style="display: flex; align-items: center; margin-bottom: -20px;">
                <img src="https://symbolshub.org/wp-content/uploads/2019/10/bullet-point-symbol.png" alt="logo" style="width: 25px; margin-right: 5px; vertical-align: middle;">
                <h3 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; margin-top: 0; font-size: 12px; font-weight: bold; vertical-align: middle; margin-bottom: 0;">អត្រាអតិផរណារបស់ប្រទេសដៃគូប្រកួតប្រជែង</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        new_table = load_data(filtered_df)
        filtered_df["Value"] = filtered_df["Value"].str.replace('%', '').astype(float)
        max_row, min_row, avg_value, update_frequency = category_data(filtered_df)
        col1, col2,col3,col4 = st.columns(4)
        with col1:
            st.info('Maximum Inflation Rate',icon="⬆️")
            st.write(f"{max_row['Country'].values[0]} : {max_row['Value'].values[0]}","%")

        with col2:
            st.info('Minimum Inflation Rate',icon="⬇️")
            st.write(f"{min_row['Country'].values[0]} : {min_row['Value'].values[0]}","%")
        with col3:
            st.info('Average Inflation Rate',icon="📈")
            st.write(avg_value,"%")
        with col4:
            st.info('Update frequency',icon="🔄") 
            st.write(update_frequency)
        
        column_width = "50%"
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div style="width: {700};"></div>', unsafe_allow_html=True)
            plot_line_chart(new_table, selected_start_date, selected_end_date)
        with col2:
            st.markdown(f'<div style="width: {400};"></div>', unsafe_allow_html=True)
            plot_bar_chart(new_table, selected_start_date, selected_end_date)
        country_notes = find_countries_with_cpli_or_base(df,selected_start_date, selected_end_date,country)
        
def competitors(df):
    #comp=compititors
    comp_countries = ["Bangladesh", "Indonesia ", "Thailand", "Vietnam", "Sri Lanka", "Philipinas", "Malaysia", "Lao", "Singapore"]
    comp_df = df[df["Country"].isin(comp_countries)]
    #st.table(comp_df, 100, 200)

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
                <h3 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; margin-top: 0; font-size: 12px; font-weight: bold; vertical-align: middle;">តារាងទិន្នន័យនៃប្រទេសដែលជាដៃគូពាណិ្ចចកម្ម</h3><br><br><br>
            </div>
            """,
            unsafe_allow_html=True
        )
        result = pivot_table(filtered_df, selected_start_date, selected_end_date)
        result_styled = result.style.set_properties(**{'background-color': 'rgb(161, 219, 255, 0.3)', 'color': 'black'})
        st.dataframe(result_styled)
        download_pivot_table_csv(result)
        st.markdown(
            """
            <div style="display: flex; align-items: center;">
                <img src="https://symbolshub.org/wp-content/uploads/2019/10/bullet-point-symbol.png" alt="logo" style="width: 25px; margin-right: 5px; vertical-align: middle;">
                <h3 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; margin-top: 0; font-size: 12px; font-weight: bold; vertical-align: middle;">អត្រាអតិផរណារបស់ប្រទេសដៃគូប្រកួតប្រជែង</h3><br><br><br>
            </div>
            """,
            unsafe_allow_html=True
        )
        new_table = load_data(filtered_df)
        filtered_df["Value"] = filtered_df["Value"].str.replace('%', '').astype(float)
        max_row, min_row, avg_value, update_frequency = category_data(filtered_df)
        col1, col2,col3,col4 = st.columns(4)
        with col1:
            st.info('Maximum Inflation Rate',icon="⬆️")
            st.write(f"{max_row['Country'].values[0]} : {max_row['Value'].values[0]}","%")

        with col2:
            st.info('Minimum Inflation Rate',icon="⬇️")
            st.write(f"{min_row['Country'].values[0]} : {min_row['Value'].values[0]}","%")
        with col3:
            st.info('Average Inflation Rate',icon="📈")
            st.write(avg_value,"%")
        with col4:
            st.info('Update frequency',icon="🔄")
            st.write(update_frequency)
        #st.dataframe(new_table)
        column_width = "50%"
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div style="width: {700};"></div>', unsafe_allow_html=True)
            plot_line_chart(new_table, selected_start_date, selected_end_date)
        with col2:
            st.markdown(f'<div style="width: {400};"></div>', unsafe_allow_html=True)
            plot_bar_chart(new_table, selected_start_date, selected_end_date)
        country_notes = find_countries_with_cpli_or_base(df,selected_start_date, selected_end_date,country)

def find_countries_with_cpli_or_base(df, selected_start_date, selected_end_date, selected_countries=None):
    country_notes = []

    # Filter the DataFrame based on the selected start and end dates
    filtered_df = df[(df['Year'] >= selected_start_date.year) & (df['Year'] <= selected_end_date.year)]

    # Remove duplicate entries based on 'Year', 'Country', and 'Note'
    filtered_df = filtered_df.drop_duplicates(subset=[ 'Country', 'Note'])

    # Iterate over each row in the filtered DataFrame
    for _, row in filtered_df.iterrows():
        year = row['Year']
        note = row['Note']

        # Check if the note contains "CPI", "Base", or "base" followed by a year in the format YYYY
        if re.search(r'(CPI|Base|base)\s+(\d{4})', str(note), re.IGNORECASE):
            country = row['Country']
            
            # If selected_countries is provided and current country is not in the list, skip it
            if selected_countries is not None and country not in selected_countries:
                continue
            
            country_notes.append({'year': year, 'country': country, 'note': note})
    
    # Print the selected countries' notes
    for item in country_notes:
        st.write("Note: "f"{item['country']} {item['note']}")
    
    return country_notes

def category_data(df):
       max_row = df[df["Value"] == df["Value"].max()]
       min_row = df[df["Value"] == df["Value"].min()]
       avg_value = df["Value"].mean()
       update_frequency = df["Update frequency"].iloc[0]
       return max_row, min_row, avg_value, update_frequency
def Dashboard():

    df = pd.read_csv(r"D:\Intership\Labour ministry of combodain\test\SampleSpreadSheet.csv")
    
    st.set_page_config(
        page_title = "Ministry of Labour and Vocational Training",
        page_icon = "https://res.cloudinary.com/aquarii/image/upload/v1643955074/Ministry-of-Labour-Vocational-Training-MoLVT-2.jpg",
        layout= "wide",
        initial_sidebar_state="auto"
    #     menu_items={
    #         'Get Help': 'https://www.extremelycoolapp.com/help',
    #         'Report a bug': 'https://www.extremelycoolapp.com/bug',
    #         'About' :"This is a header. This is an *extremely* cool app!"
    # }


    )


    st.markdown(
        """
        <div style="display: flex; align-items: center;">
            <img src="https://cdn3d.iconscout.com/3d/free/thumb/free-line-chart-growth-3814121-3187502.png" alt="logo" style="width: 90px; margin-right: 15px;">
            <h3 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; margin-top: 0;">ការវិភាគអត្រាអតិផរណារ</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    

    # Add content below the box
    #st.write('ប្រទេសដៃគូប្រកួតប្រជែង និងប្រទេសដៃគូពាណិជ្ជកម្ម')

    # Side Bar

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
        
    # Print the country-note tuples

    else:
        st.write(" ")


if __name__ == '__main__':
    Dashboard()




def download_csv(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV file</a>'
    return href
