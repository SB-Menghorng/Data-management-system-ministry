import os.path

import pandas as pd


def clean_1(dir_csv, input_file):
    df_cpi = pd.read_excel(input_file)

    set_columns = df_cpi.iloc[2].tolist()
    df_cpi.columns = set_columns

    df_cpi = df_cpi.iloc[5:].reset_index(drop=True)
    df_cpi.set_index('1. Consumer Price Index (CPI) and Component Indices', inplace=True)

    df_cpi = df_cpi.transpose()
    for col in df_cpi.columns:
        df_cpi[col] = df_cpi[col].astype(float)

    df1 = df_cpi.iloc[:, 0:13]
    df2 = df_cpi.iloc[:, 15:28]
    df3 = df_cpi.iloc[:, 30:42]
    df4 = df_cpi.iloc[:, 42:45]

    df1.index = df1.index.astype(str).str.split(' ').str[0]
    df2.index = df2.index.astype(str).str.split(' ').str[0]
    df3.index = df3.index.astype(str).str.split(' ').str[0]
    df4.index = df4.index.astype(str).str.split(' ').str[0]

    filename1 = os.path.join(os.path.join(os.path.join(dir_csv, 'monetary_and_financial_statistics_data'), input_file.split('\\')[-1].split('.')[0]+'.'+input_file.split('\\')[-1].split('.')[1]), 'CPI_and_Component_Indices(Oct_Dec_2006=100).csv')
    filename2 = os.path.join(os.path.join(os.path.join(dir_csv, 'monetary_and_financial_statistics_data'), input_file.split('\\')[-1].split('.')[0]+'.'+input_file.split('\\')[-1].split('.')[1]), 'Percentage_of_Monthly_Change_in_CPI_and_its_Components.csv')
    filename3 = os.path.join(os.path.join(os.path.join(dir_csv, 'monetary_and_financial_statistics_data'), input_file.split('\\')[-1].split('.')[0]+'.'+input_file.split('\\')[-1].split('.')[1]), 'Percentage_of_Yearly_Change_in_CPI_and_its_Components.csv')
    filename4 = os.path.join(os.path.join(os.path.join(dir_csv, 'monetary_and_financial_statistics_data'), input_file.split('\\')[-1].split('.')[0]+'.'+input_file.split('\\')[-1].split('.')[1]), 'Average_CPI_Month_Year.csv')
    os.makedirs(os.path.join(os.path.join(dir_csv, 'monetary_and_financial_statistics_data'), input_file.split('\\')[-1].split('.')[0]+'.'+input_file.split('\\')[-1].split('.')[1]), exist_ok=True)


    df1.to_csv(filename1, index_label='Date')
    df2.to_csv(filename2, index_label='Date')
    df3.to_csv(filename3, index_label='Date')
    df4.to_csv(filename4, index_label='Date')


# input_excel_file = r"D:\Intership\Labour ministry of combodain\demo\monetary_and_financial_statistics_data\12.cpiandinflationratejun-23_en_3407.xlsx"
# dir = r'D:\Intership\Labour ministry of combodain\demo'
# clean_1(dir, input_excel_file)
