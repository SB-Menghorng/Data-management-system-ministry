import os.path
import pandas as pd


def clean_3(Input_file, dir_for_csv):
    df = pd.read_excel(Input_file)

    first_column_value = df.columns[0]

    set_columns = df.iloc[0]
    df.columns = set_columns
    df = df.iloc[1:-2, :]

    csv_filename = os.path.join(dir_for_csv, os.path.join(Input_file.split('.')[0] + '-clean', f"{first_column_value.replace(' ', '_').lower()}.csv"))
    dir_store_csv = os.path.join(dir_for_csv, Input_file.split('.')[0] + '-clean')
    os.makedirs(dir_store_csv, exist_ok=True)

    df.to_csv(csv_filename, index=False)

    return csv_filename


def renameCol2Int(csv):
    df = pd.read_csv(csv)

    # Detect column names containing '.0' and rename them
    column_names_with_dot_zero = df.columns[df.columns.str.contains(r'\.0', na=False)]
    for column in column_names_with_dot_zero:
        new_column_name = column[:4]
        df.rename(columns={column: new_column_name}, inplace=True)

    return df


# input_excel_file = r"D:\Intership\Labour ministry of combodain\demo\merchandise-trade\1619169641_89450.xlsx"
# csv_filename = clean_3(input_excel_file, r'D:\Intership\Labour ministry of combodain\demo')
# df = renameCol2Int(csv_filename)
# df