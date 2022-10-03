#!/usr/bin/env python3
# coding: utf-8

import blpapi
from xbbg import blp
import pandas as pd


# A directory for files that are not tracked by git, to which we'll download data
TMP_DIR = '../tmp/'

# Index membership field(s) and the tickers for the market indices whose membership we want to download from Bloomberg's API using the BDH function
IDX_PARAMS = {
    'tickers' : [
        'NDX Index'
        ],
    'flds' : [
        'INDX_MEMBERS'
        ]
}


def download_idx_membership(settings: dict = IDX_PARAMS) -> pd.DataFrame:
    r"""
    Download from the Bloomberg API using the BDH() function. For the purposes of our example we expect the settings dict to contain values describing a request for index membership data, but strictly speaking this is not required.

    :param settings: A dictionary with parameters for a call to Bloomberg BDH function, with keys matching the BDH parameter names
    :type settings: dict 
    :return: DataFrame containing data returned by Bloomberg
    :rtype: pandas.DataFrame
    """

    return blp.bdh(**settings)


if __name__ == "__main__":

    # Use the default IDX_PARAMS to download metadata for a small number of tickers
    idx_members = download_idx_membership()

    # Download the index membership dataset to a CSV file, using pandas.DataFrame's to_csv() method
    filename = 'index_members.csv'
    idx_members.to_csv(TMP_DIR + filename)

    # Print the first 3 records from the DataFrame to stdout.
    print('Sample of downloaded index membership data:\n',idx_members.head(3),'\n')
