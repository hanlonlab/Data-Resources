#!/usr/bin/env python3
# coding: utf-8

import blpapi
from xbbg import blp
import pandas as pd


# A directory for files that are not tracked by git, to which we'll download data
TMP_DIR = '../tmp/'

# Start date, end date, tickers, and tick history-related fields we want to download from Bloomberg's API using the BDH function
BDH_PARAMS = {
    'tickers' : [
        'NVDA US Equity',
        'AAPL US Equity'
        ],
    'flds' : [
        'High',
        'Low',
        'Last_Price'
        ],
    'start_date' : '2020-03-01',
    'end_date' : '2020-03-31'
}


def download_tick_history(settings: dict = BDH_PARAMS) -> pd.DataFrame:
    r"""
    Download from the Bloomberg API using the BDH() function. For the purposes of our example we expect the settings dict to contain values describing a request for historical tick data, but strictly speaking this is not required.

    :param settings: A dictionary with parameters for a call to Bloomberg BDH function, with keys matching the BDH parameter names
    :type settings: dict 
    :return: DataFrame containing data returned by Bloomberg
    :rtype: pandas.DataFrame
    """

    return blp.bdh(**settings)


if __name__ == "__main__":

    # Use the default BDH_PARAMS to download metadata for a small number of tickers
    hist_tick_data = download_tick_history()

    # Download the tick history dataset to a CSV file, using pandas.DataFrame's to_csv() method
    filename = 'tick_data_' + BDH_PARAMS['start_date'] + '_' + BDH_PARAMS['end_date'] + '.csv'
    hist_tick_data.to_csv(TMP_DIR + filename)

    # Print the first 3 records from the DataFrame to stdout.
    print('Sample of downloaded historical tick data:\n',hist_tick_data.head(3),'\n')
