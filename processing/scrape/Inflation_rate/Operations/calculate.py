from datetime import datetime

import pandas as pd


class InflationRate:
    """
    The InflationRateCalculator class is used to calculate inflation rates based on input data.

    Attributes:
        df (pandas.DataFrame): The input DataFrame containing inflation-related data.
        consumer_column (str, optional): The column containing consumer price index data (default is None).

    Methods:
        - calculate_by_vietnam(indicator_column='INDICATOR', time_column='TIME_PERIOD', value_column='OBS_VALUE'):
            Calculates inflation rates based on Vietnam-specific data.
        - calculate_by_general(): Calculates inflation rates based on general data.
    """
    def __init__(self, df, consumer_column=None):
        self.consumer_column = consumer_column
        self.df = df

    def ByVietnam(self, indicator_column='INDICATOR', time_column='TIME_PERIOD', value_column='OBS_VALUE'):
        """
        Calculates inflation rates based on Vietnam-specific data.

        Args:
            indicator_column (str, optional): The column containing indicator information (default is 'INDICATOR').
            time_column (str, optional): The column containing time information (default is 'TIME_PERIOD').
            value_column (str, optional): The column containing value information (default is 'OBS_VALUE').

        Returns:
            dict: A dictionary containing calculated inflation rates.
        """

        df = self.df
        df_consumer = df[df[indicator_column] == 'PCPI_IX']

        years = df_consumer[time_column].dt.year.sort_values(ascending=False).unique()
        year_interval = years[0] - years[-1]

        ifrs = {time_column: [], 'Inflation Rate': []}
        for i in range(year_interval):
            month_now = df_consumer[(df[time_column].dt.year == years[i])][time_column].dt.month
            month_before = df_consumer[(df[time_column].dt.year == years[i + 1])][time_column].dt.month

            if len(month_now) <= len(month_before):
                month_intervals = month_now
                time_period = list(
                    df_consumer[(df[time_column].dt.year == years[i])][time_column].dt.strftime('%Y-%m-%d').values)
            else:
                month_intervals = month_before
                time_period = list(df_consumer[(df[time_column].dt.year == years[i]) & (
                    df[time_column].dt.month.isin(month_intervals))][time_column].dt.strftime('%Y-%m-%d').values)

            for time in time_period:
                # Define the format of your time string (YYYY-MM-DD in this case)
                format_str = "%Y-%m-%d"

                # Convert the string to a datetime object
                time = datetime.strptime(time, format_str)

                ifrs[time_column].append(time)

            for month in month_intervals:
                cpi_now = df_consumer[(df_consumer[time_column].dt.month == month)].sort_values(time_column)[
                    (df_consumer[time_column].dt.year == years[i])][value_column].values
                cpi_before = df_consumer[(df_consumer[time_column].dt.month == month)].sort_values(time_column)[
                    (df_consumer[time_column].dt.year == years[i + 1])][value_column].values
                ifr = cpi_now / cpi_before - 1
                ifrs['Inflation Rate'].append(ifr[0])

        ifrs = list(pd.DataFrame(ifrs).set_index(time_column).to_dict().values())[0]

        return ifrs

    def ByGeneral(self):
        """
        Calculates inflation rates based on general data.

        Returns:
            pandas.DataFrame: A DataFrame containing calculated inflation rates.
        """

        df = self.df
        consumer_col = self.consumer_column

        if consumer_col is None:
            consumer_col = 'CPI'
        df1 = df.copy()
        ifrs = []
        for year in sorted(df['Year'].unique(), reverse=True):
            for month in df[df['Year'] == year]['Month'].unique():
                ifr = (df[(df['Month'] == month) & (df['Year'] == year)][consumer_col].values /
                       df[(df['Month'] == month) & (df['Year'] == year - 1)][consumer_col].values - 1)
                if len(ifr) > 0:
                    ifrs.append(ifr[0])
                else:
                    ifrs.append(0)
        df1['Value'] = ifrs[::-1]
        return df1
