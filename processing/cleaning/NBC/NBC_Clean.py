import pandas as pd


def NBC_14(input_file):  # NBC_14

    sheet1_df = pd.read_excel(input_file, sheet_name='MoM')
    sheet2_df = pd.read_excel(input_file, sheet_name='YoY')

    # Concatenate the DataFrames vertically
    df = pd.concat([sheet1_df, sheet2_df], ignore_index=True)

    set_columns = df.iloc[4].tolist()
    df.columns = set_columns

    df = df.iloc[5:].reset_index(drop=True)
    df.set_index('Oct, Dec. 2006 = 100', inplace=True)
    df = df.transpose()
    # for col in df.columns:
    #     if pd.api.types.is_datetime64_any_dtype(df[col]):
    #         continue  
    #     #df[col] = df[col].astype(float)

    df1 = df.iloc[:, 0:13]
    df2 = df.iloc[:, 20:33]

    # Convert index values to strings and then remove time part
    df1.index = df1.index.astype(str).str.split(' ').str[0]
    df2.index = df2.index.astype(str).str.split(' ').str[0]

    # Move index values to a column named "Date"
    df1['Date'] = df1.index
    # Reset the index
    df1 = df1.reset_index(drop=True)
    # Rearrange the columns
    df1 = df1.reindex(columns=['Date', 'Inflation (All Items) Month on Month  %Change',
                               '  Food and Non-Alcoholic Beverages',
                               '  Alcoholic Baveraged, Tobacco and Narcotics',
                               '  Clothing and Footwear',
                               '  Housing, Water, Electricity, Gas and other Fuels',
                               '  Furnishings, Household Household Maintenance', '  Health',
                               '  Transportation', '  Communication', '  Recreation and Culture',
                               '  Education', '  Restaurants ',
                               '  Miscellaneous Goods and   Services'])

    # Move index values to a column named "Date"
    df2['Date'] = df2.index
    # Reset the index
    df2 = df2.reset_index(drop=True)
    # Rearrange the columns
    df2 = df2.reindex(columns=['Date', 'Inflation (All Items) Year on Year  %Change',
                               '  Food and Non-Alcoholic Beverages',
                               '  Alcoholic Baveraged, Tobacco and Narcotics',
                               '  Clothing and Footwear',
                               '  Housing, Water, Electricity, Gas and other Fuels',
                               '  Furnishings, Household Household Maintenance', '  Health',
                               '  Transportation', '  Communication', '  Recreation and Culture',
                               '  Education', '  Restaurants ',
                               '  Miscellaneous Goods and   Services'])

    # Output DataFrames to CSV files
    # df1.to_csv('Contribution_Inflation_Month_on_Month(%Change).csv', index_label='Date')
    # df2.to_csv('Inflation_All_Items_Year_on_Year(%Change).csv', index_label='Date')

    return df1, df2
