#!/usr/bin/env python3
# coding: utf-8

import blpapi
from xbbg import blp
import pandas as pd


# A directory for files that are not tracked by git, to which we'll download data
TMP_DIR = '../tmp/'

# Tickers, dividend-related fields, and dividend-specific start and end dates for the dividend data we want to download from Bloomberg's API using the BDS function
DIV_PARAMS = {
    'tickers' : [
        'NVDA US Equity',
        'AAPL US Equity'
        ],
    'flds' : [
        'DVD_Hist_All'
        ],
    'DVD_Start_Dt' : '20180101',
    'DVD_End_Dt' : '20180531'
}


def download_div_data(settings: dict = DIV_PARAMS) -> pd.DataFrame:
    r"""
    Download from the Bloomberg API using the BDS() function. For the purposes of our example we expect the settings dict to contain values describing a request for dividend data, but strictly speaking this is not required.

    :param settings: A dictionary with parameters for a call to Bloomberg BDS function, with keys matching the BDS parameter names
    :type settings: dict 
    :return: DataFrame containing data returned by Bloomberg
    :rtype: pandas.DataFrame
    """

    blp.bdh(**settings)


if __name__ == "__main__":

    # Use the default DIV_PARAMS to download dividend data for a small number of tickers
    dividend_data = download_div_data()

    # Download the dividend dataset to a CSV file, using pandas.DataFrame's to_csv() method
    filename = 'dividend_data_' + DIV_PARAMS['DVD_Start_Dt'] + '_' + DIV_PARAMS['DVD_End_Dt'] + '.csv'
    dividend_data.to_csv(TMP_DIR + filename)

    # Print the first 3 records from the DataFrame to stdout.
    print('Sample of downloaded dividend data:\n',dividend_data.head(3),'\n')
