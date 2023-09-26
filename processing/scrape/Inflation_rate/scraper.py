from processing.constant import excel, sheet_name, host, password, user, your_table_name, database_name
from processing.scrape.Inflation_rate import AfterOptimize_IndoInf, Vietnam, Philippines
from processing.excel_connection import Excel
from processing.database import Database


def InflationRate():
    excel_conn = Excel(excel_file=excel, sheet_name=sheet_name)
    db = Database(host, password, user, table=your_table_name, database=database_name)

    # Vietnam.main(create_table=True, insert_data=True, table_show=True, delete_table=False)
    # AfterOptimize_IndoInf.main()
    # Philippines.main()
    #
    # df = db.read_database(your_condition='Year >= 2018')
    # excel_conn.update_excel_with_row_level_validation(df)
    # excel_conn.delete_rows_from_excel_multiple_conditions(list(zip([0] * df.shape[0], df['No.'].values)))
    # return df


InflationRate()
