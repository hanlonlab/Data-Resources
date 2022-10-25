#!/usr/bin/env python3
# coding: utf-8

import blpapi
from xbbg import blp
import pandas as pd


# A directory for files that are not tracked by git, to which we'll download data
TMP_DIR = '../tmp/'

# Start date, end date, tickers, codes for the last traded price & market cap fields we want to download from Bloomberg's API using the BDH function
PXM_PARAMS = {
    'tickers' : [
        'NVDA US Equity',
        'AAPL US Equity'
        ],
    'flds' : [
        'PX_LAST',
        'CUR_MKT_CAP'
        ],
    'start_date' : '2020-03-01',
    'end_date' : '2020-03-31'
}


def download_px_cap_data(settings: dict = PXM_PARAMS) -> pd.DataFrame:
    r"""
    Download from the Bloomberg API using the BDH() function. For the purposes of our example we expect the settings dict to contain values describing a request for last traded price and market capitalization data, but strictly speaking this is not required.

    :param settings: A dictionary with parameters for a call to Bloomberg BDH function, with keys matching the BDH parameter names
    :type settings: dict 
    :return: DataFrame containing data returned by Bloomberg
    :rtype: pandas.DataFrame
    """

    return blp.bdh(**settings)


if __name__ == "__main__":

    # Use the default PXM_PARAMS to download metadata for a small number of tickers
    px_cap_data = download_px_cap_data()

    # Download the last traded price & market cap dataset to a CSV file, using pandas.DataFrame's to_csv() method
    filename = 'px_cap_' + PXM_PARAMS['start_date'] + '_' + PXM_PARAMS['end_date'] + '.csv'
    px_cap_data.to_csv(TMP_DIR + filename)

    # Print the first 3 records from the DataFrame to stdout.
    print('Sample of last price & market cap data:\n',px_cap_data.head(3),'\n')
