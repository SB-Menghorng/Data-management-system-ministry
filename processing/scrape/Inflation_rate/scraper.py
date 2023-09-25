from processing.scrape.Inflation_rate import AfterOptimize_IndoInf, Vietnam


def InflationRate():
    # AfterOptimize_IndoInf.main()
    return Vietnam.main(create_table=False, insert_data=True)


df = InflationRate()
print(df['PublishDate'])