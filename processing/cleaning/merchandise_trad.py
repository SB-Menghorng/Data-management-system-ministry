import pandas as pd


def clean_3(Input_file):
    df = pd.read_excel(Input_file)

    first_column_value = df.columns[0]

    set_columns = df.iloc[0]
    df.columns = set_columns
    df = df.iloc[1:-2, :]

    csv_filename = f"{first_column_value.replace(' ', '_').lower()}.csv"

    df.to_csv(csv_filename, index=False)


input_excel_file = '1619169687_70360.xlsx'
clean_3(input_excel_file)


def renameCol2Int(csv):
    df = pd.read_excel(csv)
    # Detect column names containing '.0' and rename them
    column_names_with_dot_zero = df.columns[df.columns.str.contains(r'\.0', na=False)]
    for column in column_names_with_dot_zero:
        new_column_name = column[:4]
        df.rename(columns={column: new_column_name}, inplace=True)
    return df


def clean_3(Input_file):
    df = pd.read_excel(Input_file)

    first_column_value = df.columns[0]

    set_columns = df.iloc[0]
    df.columns = set_columns
    df = df.iloc[1:-2, :]

    csv_filename = f"{first_column_value.replace(' ', '_').lower()}.csv"

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


# input_excel_file = '1588824247_06051.xlsx'
# csv_filename = clean_3(input_excel_file)
# df = renameCol2Int(csv_filename)
# df