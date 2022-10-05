#!/usr/bin/env python3
# coding: utf-8

import blpapi
from xbbg import blp
import pandas as pd
import datetime


# A directory for files that are not tracked by git, to which we'll download data
TMP_DIR = '../tmp/'

# Index membership field(s) and the tickers for the market indices whose membership we want to download from Bloomberg's API using the BDH function
IDX_PARAMS = {
    'tickers' : [
        'SPX Index'
        ],
    'flds' : [
        'INDX_MEMBERS'
        ]
}
MOV_AVG_PARAMS = {  
    'flds' : [
        'PX_LAST',
        'MOV_AVG_200D',
        'CUR_MKT_CAP'
        ],
    'start_date' : '2022-01-01',
    'end_date' : datetime.datetime.today().strftime('%Y-%m-%d')
}


def download_idx_membership(settings: dict = IDX_PARAMS) -> pd.DataFrame:
    r"""
    Get members of an index

    :param settings: A dictionary with parameters for a call to Bloomberg BDS function, with keys matching the BDS parameter names
    :type settings: dict 
    :return: DataFrame containing data returned by Bloomberg
    :rtype: pandas.DataFrame
    """

    return blp.bds(**settings)


def moving_avg_by_idx(settings: str = IDX_PARAMS) -> pd.DataFrame:
    r"""
    Print percentage of index and list of symbols trading above 200 day moving average

    :param settings: 
    :type settings: dict 
    :return: DataFrame containing data returned by Bloomberg
    :rtype: pandas.DataFrame
    """

    idx_members_df = download_idx_membership(settings)
    idx_members = idx_members_df['member_ticker_and_exchange_code']

    for sym in idx_members:
        print(blp.bdh(tickers = [sym], **MOV_AVG_PARAMS))
    


if __name__ == "__main__":

    # Use the default IDX_PARAMS to download metadata for a small number of tickers
    idx_members = download_idx_membership()

    # Download the index membership dataset to a CSV file, using pandas.DataFrame's to_csv() method
    filename = 'index_members.csv'
    idx_members.to_csv(TMP_DIR + filename)

    # Print the first 3 records from the DataFrame to stdout.
    print('Sample of downloaded index membership data:\n',idx_members.head(10),'\n')
