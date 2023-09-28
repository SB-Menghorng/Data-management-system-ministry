from datetime import datetime

import pandas as pd


def inflation_rate(df, indicator_column='INDICATOR', time_column='TIME_PERIOD', value_column='OBS_VALUE'):
    df_consumer = df[df[indicator_column] == 'PCPI_IX']

    years = df_consumer[time_column].dt.year.sort_values(ascending=False).unique()
    year_interval = years[0] - years[-1]

    ifrs = {time_column: [], 'Inflation Rate': []}
    for i in range(year_interval):
        monthn = df_consumer[(df[time_column].dt.year == years[i])][time_column].dt.month
        monthb = df_consumer[(df[time_column].dt.year == years[i + 1])][time_column].dt.month

        if len(monthn) <= len(monthb):
            month_intervals = monthn
            time_period = list(
                df_consumer[(df[time_column].dt.year == years[i])][time_column].dt.strftime('%Y-%m-%d').values)
        else:
            month_intervals = monthb
            time_period = list(df_consumer[(df[time_column].dt.year == years[i]) & (
                df[time_column].dt.month.isin(month_intervals))][time_column].dt.strftime('%Y-%m-%d').values)

        for time in time_period:
            # Replace this with your time string

            # Define the format of your time string (YYYY-MM-DD in this case)
            format_str = "%Y-%m-%d"

            # Convert the string to a datetime object
            time = datetime.strptime(time, format_str)

            ifrs[time_column].append(time)

        for month in month_intervals:
            cpin = df_consumer[(df_consumer[time_column].dt.month == month)].sort_values(time_column)[
                (df_consumer[time_column].dt.year == years[i])][value_column].values
            cpib = df_consumer[(df_consumer[time_column].dt.month == month)].sort_values(time_column)[
                (df_consumer[time_column].dt.year == years[i + 1])][value_column].values
            ifr = cpin / cpib - 1
            ifrs['Inflation Rate'].append(ifr[0])

    ifrs = list(pd.DataFrame(ifrs).set_index(time_column).to_dict().values())[0]

    return ifrs
