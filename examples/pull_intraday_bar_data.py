#!/usr/bin/env python3
# coding: utf-8

import blpapi
from xbbg import blp
import pandas as pd


# A directory for files that are not tracked by git, to which we'll download data
TMP_DIR = '../tmp/'

# Tickers for which we want to download intraday bar data
TICKERS = [
        'BTC Curncy',
        'ETH Curncy',
        'XBTUSD Curncy',
        'XETUSD Curncy'
        ]

# dt: BDIB date parameter, date to download
# session: BDIB session parameter, one of [allday, day, am, pm, pre, post])
# typ: BDIB type parameter, one of [TRADE, BID, ASK, BID_BEST, ASK_BEST, BEST_BID, BEST_ASK]
BDIB_PARAMS = {
    'dt': '2022-09-30',
    'session': 'allday',
    'typ': 'TRADE'
    }

# ref: BDIB reference exchange parameter, I'm using IndexUS when the xbbg default exchange lookup fails
BDIB_REF_EXCH = 'IndexUS'

def download_intraday_bar(ticker: str, settings: dict = BDIB_PARAMS) -> pd.DataFrame:
    r"""
    Download intraday bar data from the Bloomberg API using the BDIB() function

    :param settings: The ticker for which we want to download intraday bar data
    :type settings: str
    :param settings: A dictionary with non-ticker parameters for a call to Bloomberg BDIB function, with keys matching the BDIB parameter names
    :type settings: dict 
    :return: DataFrame containing data returned by Bloomberg
    :rtype: pandas.DataFrame
    """

    try:
        bar_df = blp.bdib(ticker=ticker, **settings)
    except:
        bar_df = blp.bdib(ticker=ticker, **settings, ref=BDIB_REF_EXCH)

    return bar_df


if __name__ == "__main__":

    for ticker in TICKERS:
        # Request intraday bar data for ticker from Bloomberg API
        bar_data = download_intraday_bar(ticker, settings=BDIB_PARAMS)

        # Download the intraday bar dataframe to file
        filename = 'intraday_bar_' + ticker.split()[0] + '_' + '_'.join(str(param).lower() for param in BDIB_PARAMS.values()) + '.csv'
        bar_data.to_csv(TMP_DIR + filename)

        # Print the first 3 records from the DataFrame to stdout.
        print('Sample of downloaded ' + ticker + ' intraday bar data:\n', bar_data.head(3), '\n')