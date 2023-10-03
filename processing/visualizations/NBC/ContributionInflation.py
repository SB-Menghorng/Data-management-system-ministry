import streamlit as st
import pandas as pd
import os
import warnings
import plotly.express as px
from processing.constant import thyda_dir, fltest
warnings.filterwarnings('ignore')


def visualize_economic_data(dir_file):
    # logo
    image_path = "https://freepngimg.com/download/technology/63583-visualization-data-illustration-png-image-high-quality.png"
    st.sidebar.image(image_path)

    # Title
    st.title(":chart_with_upwards_trend: Visualizing Domestic Currencies")
    # st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=False)

    # File uploader
    fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))

    # Load the data
    if fl is not None:
        filename = fl.name
        st.write(filename)
        df = pd.read_csv(filename, encoding='ISO-8859-1')
    else:
        # don't forget to Change path jahh!
        os.chdir(thyda_dir)
        df = pd.read_csv(dir_file,
                         encoding="ISO-8859-1")

    # Date handling
    date_columns = df.columns[2:]
    date_values = pd.to_datetime(date_columns, errors='coerce')
    start_date = date_values.min()
    end_date = date_values.max()

    # Date selection
    col1, col2 = st.columns(2)
    with col1:
        selected_start_date = st.date_input("Start Date", start_date)
    with col2:
        selected_end_date = st.date_input("End Date", end_date)

    selected_start_date = pd.to_datetime(selected_start_date)
    selected_end_date = pd.to_datetime(selected_end_date)

    # Sidebar Filter
    st.sidebar.header("Choose your filter: ")

    # Country selection
    countries = st.sidebar.multiselect("Select Countries", df["Countries"].unique())
    if not countries:
        df2 = df.copy()
    else:
        df2 = df[df["Countries"].isin(countries)]

    # Currency selection
    # currencies = st.sidebar.multiselect("Select Currencies", df["Currencies"].unique())
    # if not currencies:
    #     df3 = df.copy()
    # else:
    #     df3 = df[df["Currencies"].isin(currencies)]

    # Filter the data based on Countries
    if not countries:
        filter_df = df
    else:
        filter_df = df[df["Countries"].isin(countries)]

    # Display the filtered data
    st.write("Filtered Data:")
    st.dataframe(filter_df)

    # Filter the data based on Date
    selected_date_columns = date_columns[(date_values >= selected_start_date) & (date_values <= selected_end_date)]
    filter_df = filter_df[["Countries", "Currencies"] + list(selected_date_columns)]
    filter_df = filter_df.melt(id_vars=["Countries", "Currencies"], var_name="Date", value_name="Value")

    category_df = filter_df.groupby(by=["Countries"], as_index=False)["Value"].mean()

    # Create columns for layout
    col1, col2 = st.columns(2)

    # Bar chart in col1
    with col1:
        st.subheader("Countries with its average currencies")
        fig = px.bar(category_df, x="Countries", y="Value", text=['{:,.2f}'.format(x) for x in category_df["Value"]],
                     template="seaborn")
        st.plotly_chart(fig, use_container_width=True, height=400)

    with col2:
        st.subheader("Countries with its average percentage currencies")
        # Calculate the total sum of average values
        total_average = category_df["Value"].sum()

        # Calculate the percentage of each country's average value
        category_df["Percentage"] = (category_df["Value"] / total_average) * 100

        # Plot the pie chart with percentages
        fig = px.pie(category_df, values="Percentage", names="Countries", hole=0.5)
        fig.update_traces(textinfo="percent+label")

        st.plotly_chart(fig, use_container_width=True)

    cl1, cl2 = st.columns(2)
    with cl1:
        with st.expander("Average_Countries_ViewData"):
            countries = filter_df.groupby(by="Countries", as_index=False)["Value"].mean()
            st.write(countries.style.background_gradient(cmap="Blues"))
            csv = countries.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="Data.csv", mime="text/csv",
                               help='Click here to download the data as a CSV file')

    with cl2:
        with st.expander("Currencies_Percentage_ViewData"):
            countries_df = filter_df.groupby(by="Countries", as_index=False)["Value"].mean()
            countries_df["Percentage"] = (countries_df["Value"] / countries_df["Value"].sum()) * 100
            countries_df = countries_df.drop(columns=["Value"])  # Remove the "Value" column
            st.write(countries_df.style.background_gradient(cmap="Oranges"))

            csv = countries_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="Currencies_Data.csv", mime="text/csv",
                               help='Click here to download the data as a CSV file')

    # time series
    if not countries.empty:
        grouped_df = filter_df.groupby(["Countries", "Date"]).sum().reset_index()
        x_label = "Countries"
    else:
        grouped_df = filter_df.groupby(["Currencies", "Date"]).sum().reset_index()
        x_label = "Currencies"

    st.subheader(f"Time Series by {x_label}")
    fig = px.line(
        grouped_df,
        x="Date",
        y="Value",
        color=x_label,
        title=f"Time Series by {x_label}",
        color_discrete_sequence=px.colors.qualitative.Set1  # Use a color scale
    )
    fig.update_traces(line=dict(width=3))
    fig.update_layout(width=1600, height=600)
    st.plotly_chart(fig)


# if __name__ == "__main__":
#     visualize_economic_data(df)
