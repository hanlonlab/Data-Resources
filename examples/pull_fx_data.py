#!/usr/bin/env python3
# coding: utf-8

import blpapi
from xbbg import blp
import pandas as pd
import datetime
import itertools


# A directory for files that are not tracked by git, to which we'll download data
TMP_DIR = '../tmp/'

# Start date, end date, tickers, codes for the last traded price & market cap fields we want to download from Bloomberg's API using the BDH function
FX_PARAMS = {
    'tickers' : [
        'AUD','CAD','CHF','EUR','GBP','JPY','NOK','NZD','SEK','USD'
        ],
    'flds' : [
        'BEST_ASK',
        'BEST_BID'
        ],
    'start_date' : '2020-03-01',
    'end_date' : '2020-03-31'
}


def download_fx_intraday_data(settings: dict = FX_PARAMS) -> pd.DataFrame:
    r"""
    Download from the Bloomberg API using the BDH() function. For the purposes of our example we expect the settings dict to contain values describing a request for currency intraday data, but strictly speaking this is not required.

    :param settings: A dictionary with parameters for a call to Bloomberg BDH function, with keys matching the BDH parameter names
    :type settings: dict 
    :return: DataFrame containing data returned by Bloomberg
    :rtype: pandas.DataFrame
    """

    return blp.bdh(**settings)


if __name__ == "__main__":

    # combine G10 currencies into pairs by filtering the G10 X G10 Cartesian product using list comprehension
    currency_pairs = sorted([[a,b] for a,b in itertools.product(FX_PARAMS['tickers'], repeat=2) if a!=b])[26:]

    # get dates to use when filtering our BDH call
    anchor_date = pd.tseries.offsets.BDay(-1).apply(pd.datetime.now())
    start_date = pd.datetime.combine(anchor_date - datetime.timedelta(days=365), datetime.time(13, 30))
    end_date = pd.datetime.combine(anchor_date, datetime.time(14, 30))


    # Use the default FX_PARAMS to download metadata for a small number of tickers
    fx_intraday_data = download_fx_intraday_data()

    # Download the last traded price & market cap dataset to a CSV file, using pandas.DataFrame's to_csv() method
    filename = 'fx_intraday_' + FX_PARAMS['start_date'] + '_' + FX_PARAMS['end_date'] + '.csv'
    fx_intraday_data.to_csv(TMP_DIR + filename)

    # Print the first 3 records from the DataFrame to stdout.
    print('Sample of fx intraday data:\n',fx_intraday_data.head(3),'\n')
