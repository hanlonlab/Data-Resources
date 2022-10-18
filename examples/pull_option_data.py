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
        'AGG US Equity',
        'AAPL US Equity'
        ],
    'flds' : [
        'PX_BID'#,
        #'PX_ASK',
        #'PX_VOLUME'
        ],
    'start_date' : '2020-03-01',
    'end_date' : '2020-03-31'
}


def filter_securities(settings: dict = OPT_PARAMS, max_days: int = MAX_DAYS, per_money: float = PER_MONEY) -> list:
    r"""
    Get and filter option tickers using scripts parameters.

    :param settings: A dictionary with parameters for a call to Bloomberg BDS function, with keys matching the BDS parameter names
    :type settings: dict 
    :return: list of filtered tickers for which option data is needed
    :rtype: list
    """

    # get a DataFrame with PX_LAST from BDS using tickers - note tickers will comprise the index
    px_last_vals = blp.bds(tickers=settings['tickers'], flds=['PX_LAST'])

    
    for ticker in settings['tickers']:
        # filter the PX_LAST DataFrame by ticker within the index, grab the first row from the resulting one-row DataFrame, extract value of column named "value"
        last_price = float(px_last_vals.filter(items=[ticker],axis=0).iloc[0]['value'])

        low_strike = last_price * (1.0 - per_money)
        high_strike = last_price * (1.0 + per_money)

        # get options by ticker as list
        ticker_opt_chain = blp.bds(tickers=[ticker], flds=['OPT_CHAIN'])['security_description'].tolist()
        
        filtered_opts = []

        for sym in ticker_opt_chain[:10]:

            # split options of the form "AAPL US 02/17/23 P175 Equity" to pull days to expiration and strike price
            days_to_expiration = int((pd.to_datetime(sym.split(' ')[2]) - pd.to_datetime('today')).days)
            strike_price = float(sym.split(' ')[-2][1:])

            # if option within expiration and strike windows, append to filter list
            strike_in_window = (strike_price > low_strike) and (strike_price < high_strike)
            if days_to_expiration < max_days and strike_in_window:
                filtered_opts.append(sym)
    
    return (settings['tickers'] + filtered_opts)


def download_option_data(settings: dict = OPT_PARAMS) -> pd.DataFrame:
    r"""
    Download from the Bloomberg API using the BDH() function. For the purposes of our example we expect the settings dict to contain values describing a request for currency intraday data, but strictly speaking this is not required.

    :param settings: A dictionary with parameters for a call to Bloomberg BDH function, with keys matching the BDH parameter names
    :type settings: dict 
    :return: DataFrame containing data returned by Bloomberg
    :rtype: pandas.DataFrame
    """

    # add filtered securities list to the dict containing BDH parameters
    settings['tickers'] = filter_securities(OPT_PARAMS, max_days = MAX_DAYS, per_money = PER_MONEY)

    print(settings['tickers'])

    return blp.bdh(**settings)


if __name__ == "__main__":

    bid_ask_vol_data = download_option_data(OPT_PARAMS)

    print(bid_ask_vol_data)

    # # Use the default PXM_PARAMS to download metadata for a small number of tickers
    # fx_intraday_data = download_fx_intraday_data()

    # # Download the last traded price & market cap dataset to a CSV file, using pandas.DataFrame's to_csv() method
    # filename = 'fx_intraday_' + OPT_PARAMS['start_date'] + '_' + OPT_PARAMS['end_date'] + '.csv'
    # fx_intraday_data.to_csv(TMP_DIR + filename)

    # # Print the first 3 records from the DataFrame to stdout.
    # print('Sample of fx intraday data:\n',fx_intraday_data.head(3),'\n')
