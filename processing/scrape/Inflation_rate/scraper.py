from processing.constant import excel, sheet_name, host, password, user, your_table_name, database_name
from processing.scrape.Inflation_rate import AfterOptimize_IndoInf, Vietnam, Philippines, SriLanka
from processing.excel_connection import Excel
from processing.database import Database


def InflationRate():
    excel_conn = Excel(excel_file=excel, sheet_name=sheet_name)
    # db = Database(host, password, user, table=your_table_name, database=database_name)
    # db.delete_table()
    # db.create_table()
    # Vietnam.Scraper().database_connection()
    # AfterOptimize_IndoInf.main()
    # Philippines.main()
    # df_sri = SriLanka.scrape_inflation_data()
    # db.insert_data(df_sri)

    # df = db.read_database(your_condition='Year >= 2018')
    # excel_conn.insert_into_existing_excel(df)
    # excel_conn.delete_rows_from_excel_multiple_conditions(list(zip([0] * df.shape[0], df['No.'].values)))
    # print(excel_conn.show_excel())
    # return df
    # db.show_table()


# InflationRate()

