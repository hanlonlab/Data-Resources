#!/usr/bin/env python3
# coding: utf-8

import blpapi
from xbbg import blp
import pandas as pd


# A directory for files that are not tracked by git, to which we'll download data
TMP_DIR = '../tmp/'

# Tickers and ESG-related fields we want to download from Bloomberg's API using the BDP function
ESG_PARAMS = {
    'tickers' : [
        'NVDA US Equity',
        'AAPL US Equity'
        ],
    'flds' : [
        'GHG_SCOPE_1',
        'PCT_WOMEN_ON_BOARD',
        'COMMUNITY_SPEND_%_PRETAX_PROFIT'
        ]
}


def download_esg_data(settings: dict = ESG_PARAMS) -> pd.DataFrame:
    r"""
    Download from the Bloomberg API using the BDP() function. For the purposes of our example we expect the settings dict to contain ESG-related fields, but strictly speaking this is not required.

    :param settings: A dictionary with parameters for a call to Bloomberg BDP function, with keys matching the BDP parameter names
    :type settings: dict 
    :return: DataFrame containing data returned by Bloomberg
    :rtype: pandas.DataFrame
    """

    blp.bdp(**settings)



if __name__ == "__main__":

    # Use the default ESG_PARAMS to download a small ESG dataset
    small_esg_data = download_esg_data()

    # Download the small ESG dataset to a CSV file, using pandas.DataFrame's to_csv() method
    small_esg_data.to_csv(TMP_DIR + 'small_esg_data.csv')

    # Print the first 3 records from the DataFrame to stdout.
    print('Sample of small_esg_data:\n',small_esg_data.head(3),'\n')

    # Read ESG fields from a text file into list data structure, appending them to the list field-by-field
    esg_fields = []
    with open('./esg_bloomberg_fields.txt', 'r') as file:
        for line in file:
            esg_fields.append(line.rstrip())

    # Compose dictionary for our large ESG data request, using our new list of ESG fields with the same tickers as our original request
    large_esg_params = ESG_PARAMS.copy()
    large_esg_params['flds'] = esg_fields

    # Use the large_esg_params dictionary to download a large(r) ESG dataset, then download it and print 3 records as above
    large_esg_data = download_esg_data(large_esg_params)
    large_esg_data.to_csv(TMP_DIR + 'large_esg_data.csv')
    print('Sample of large_esg_data:\n',large_esg_data.head(3),'\n')

