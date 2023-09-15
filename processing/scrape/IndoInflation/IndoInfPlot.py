import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
pd.set_option("display.max_rows", None)

df = pd.read_csv("/Users/mac/Desktop/MoLVT/Indo Inflation/IndoInflation.csv")
df['InflationData'] = df['InflationData'].str.replace(" %", "")
df['InflationData'] = df['InflationData'].astype('float64')

# Convert the 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%B %Y', errors='coerce')
# Sort the DataFrame based on the 'Date' column
df.sort_values(by='Date', inplace=True)
# Convert the 'Date' column back to the original format
df['Date'] = df['Date'].dt.strftime('%B %Y')
# Filter for years 2022 and 2023
df_filtered = df[(df['Date'].dt.year == 2022) | (df['Date'].dt.year == 2023)].copy()
# Convert the 'Date' column back to the original format
df_filtered.loc[:, 'Date'] = df_filtered['Date'].dt.strftime('%B %Y')  # Use .loc to set values

# Create a Streamlit app
st.title('Inflation Data for Years 2022 and 2023')
st.plotly_chart(px.line(df_filtered,
                        x='Date',
                        y='InflationData',
                        title='Inflation Data',
                        markers=True,
                        line_shape='linear').update_xaxes(tickangle=90))

# Add grid and labels
st.text('Plotly Plot')
