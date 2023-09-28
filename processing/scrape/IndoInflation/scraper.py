from processing.scrape.IndoInflation import AfterOptimize_IndoInf, Vietnam
# from processing.constant import your_database, your_user, your_host, your_password, your_db_table

def InflationRate():
    # AfterOptimize_IndoInf.main()
    return Vietnam.main(create_table=False, insert_data=True, table_show=False, delete_table=False)

print(InflationRate())
