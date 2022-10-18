#!/usr/bin/env python3
# coding: utf-8

import blpapi
from xbbg import blp
import pandas as pd


# A directory for files that are not tracked by git, to which we'll download data
TMP_DIR = '../tmp/'

MAX_DAYS = 140
PER_MONEY = 0.3

# Start date, end date, tickers, codes for the last traded price & market cap fields we want to download from Bloomberg's API using the BDH function
OPT_PARAMS = {
    'tickers' : [
        'AGG US Equity'
        ],
    'flds' : [
        'PX_BID',
        'PX_ASK',
        'PX_VOLUME'
        ],
    'start_date' : '2020-03-01',
    'end_date' : '2020-03-31'
}


def filter_option_tickers(settings: dict = OPT_PARAMS, day_filter: int = MAX_DAYS, per_money_filter: int = PER_MONEY) -> list:
    r"""
    Get and filter option tickers using scripts parameters.

    :param settings: A dictionary with parameters for a call to Bloomberg BDS function, with keys matching the BDS parameter names
    :type settings: dict 
    :return: list of filtered tickers for which option data is needed
    :rtype: list
    """
    px_last_vals = blp.bds(tickers=settings['tickers'], flds=['PX_LAST'])
    
    for ticker in settings['tickers']:
        print(px_last_vals.loc(px_last_vals.iloc[0] == ticker))
        print(blp.bds(tickers=settings['tickers'], flds=['OPT_CHAIN']))


def download_option_data(settings: dict = OPT_PARAMS) -> pd.DataFrame:
    r"""
    Download from the Bloomberg API using the BDH() function. For the purposes of our example we expect the settings dict to contain values describing a request for currency intraday data, but strictly speaking this is not required.

    :param settings: A dictionary with parameters for a call to Bloomberg BDH function, with keys matching the BDH parameter names
    :type settings: dict 
    :return: DataFrame containing data returned by Bloomberg
    :rtype: pandas.DataFrame
    """

    return blp.bdh(**settings)


if __name__ == "__main__":

    filter_option_tickers()

    # # Use the default PXM_PARAMS to download metadata for a small number of tickers
    # fx_intraday_data = download_fx_intraday_data()

    # # Download the last traded price & market cap dataset to a CSV file, using pandas.DataFrame's to_csv() method
    # filename = 'fx_intraday_' + OPT_PARAMS['start_date'] + '_' + OPT_PARAMS['end_date'] + '.csv'
    # fx_intraday_data.to_csv(TMP_DIR + filename)

    # # Print the first 3 records from the DataFrame to stdout.
    # print('Sample of fx intraday data:\n',fx_intraday_data.head(3),'\n')
