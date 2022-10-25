#!/usr/bin/env python3
# coding: utf-8

import blpapi
from xbbg import blp
import pandas as pd


# A directory for files that are not tracked by git, to which we'll download data
TMP_DIR = '../tmp/'

# The tickers and fields containing metadata-type information we want to download
BDP_PARAMS = {
    'tickers' : [
        'NVDA US Equity',
        'AAPL US Equity'
        ],
    'flds' : [
        'Security_Name',
        'Security_Type',
        'Security_Des',
        'EQY_Prim_Security_Ticker',
        'EQY_Prim_Security_Prim_Exch',
        'EQY_Prim_Security_Comp_Exch',
        'Market_Sector',
        'Industry_Sector',
        'GICS_Sector_Name',
        'GICS_Sub_Industry_Name ',
        'GICS_Industry_Name'
        ]
}


def download_metadata(settings: dict = BDP_PARAMS) -> pd.DataFrame:
    r"""
    Download from the Bloomberg API using the BDP() function. For the purposes of our example we expect the settings dict to contain descriptive "metadata"-like fields, but strictly speaking this is not required.

    :param settings: A dictionary with parameters for a call to Bloomberg BDP function, with keys matching the BDP parameter names
    :type settings: dict 
    :return: DataFrame containing data returned by Bloomberg
    :rtype: pandas.DataFrame
    """

    return blp.bdp(**settings)


if __name__ == "__main__":

    # Use the default BDP_PARAMS to download metadata for a small number of tickers
    ticker_metadata = download_metadata()

    # Download the metadata dataset to a CSV file, using pandas.DataFrame's to_csv() method
    ticker_metadata.to_csv(TMP_DIR + 'ticker_metadata.csv')

    # Print the first 3 records from the DataFrame to stdout.
    print('Sample of ticker_metadata:\n',ticker_metadata.head(3),'\n')
