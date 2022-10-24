#!/usr/bin/env python3
# coding: utf-8

import blpapi
from xbbg import blp
import pandas as pd
import datetime
import itertools
#from pandas.tseries.offsets import BDay


# A directory for files that are not tracked by git, to which we'll download data
TMP_DIR = '../tmp/'

# Currencies for which we want to pull data
G10_CURRENCIES = ['AUD','CAD','CHF','EUR','GBP','JPY','NOK','NZD','SEK','USD']

# typ: BDIB event type parameter, one of [TRADE, BID, ASK, BID_BEST, ASK_BEST, BEST_BID, BEST_ASK]
BDIB_TYPES = ['BEST_ASK','BEST_BID']

# session: BDIB session parameter, one of [allday, day, am, pm, pre, post])
BDIB_SESSION = 'allday'

# ref: BDIB reference exchange parameter, I'm using IndexUS when the xbbg default exchange lookup fails
BDIB_REF_EXCH = 'IndexUS'

# The number of days of data we want to pull up to our data end date, the business day previous to the code's execution date
DAYS_BACK = 2


def download_fx_intraday_data(ticker: str, typ: str, dt: str, session: str = 'allday') -> pd.DataFrame:
    r"""
    Download intraday bar data from the Bloomberg API using the BDIB() function

    :param ticker: The ticker for which we want to download intraday bar data
    :type ticker: str
    :param typ: BDIB event type parameter, one of [TRADE, BID, ASK, BID_BEST, ASK_BEST, BEST_BID, BEST_ASK]
    :type typ: str 
    :param session: BDIB session parameter, one of [allday, day, am, pm, pre, post])
    :type session: str 
    :param dt: BDIB dt parameter, date of intraday bar data we want to download formatted as 'YYYY-MM-DD' string
    :type dt: str 
    :return: DataFrame containing data returned by Bloomberg
    :rtype: pandas.DataFrame
    """

    try:
        bar_df = blp.bdib(ticker=ticker, typ=typ, dt=dt, session=session)
    except:
        bar_df = blp.bdib(ticker=ticker, typ=typ, dt=dt, session=session, ref=BDIB_REF_EXCH)

    return bar_df

def date_range(start: str, end: str):
    r"""
    Generate a date range from start date to end date, inclusive

    :param start: Start date for our date range, inclusive
    :type start: str
    :param end: End date for our date range, inclusive
    :type end: str
    :return: Generated date as 'YYYY-MM-DD' string
    :rtype: Iterator[str]
    """

    start_date = datetime.datetime.strptime(start,'%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end,'%Y-%m-%d').date()

    for num_days in range(int(((end_date+datetime.timedelta(days=1)) - start_date).days)):
        yield (start_date + datetime.timedelta(days=num_days)).strftime('%Y-%m-%d')


if __name__ == "__main__":

    # combine G10 currencies into pairs by filtering the G10 X G10 Cartesian product using list comprehension
    currency_pairs = sorted([[a,b] for a,b in itertools.product(G10_CURRENCIES, repeat=2) if a!=b])[26:]

    # get dates to use for our BDIB call, a year of data ending on the previous business day
    anchor_date = pd.tseries.offsets.BDay(-1).apply(pd.datetime.today())
    end_date = anchor_date.strftime('%Y-%m-%d')
    start_date = (anchor_date - datetime.timedelta(days=DAYS_BACK)).strftime('%Y-%m-%d')

    # iterate over dates, tickers, events to call BDIB
    for each_date in date_range(start=start_date, end=end_date):
        print(each_date)
        for ticker in G10_CURRENCIES[:2]:
            for event in BDIB_TYPES:
                # # Use the default FX_PARAMS to download metadata for a small number of tickers
                # fx_intraday_data = download_fx_intraday_data(ticker=ticker, typ=event, dt=each_date, session=BDIB_SESSION)
                # print('Sample of fx intraday data:\n',fx_intraday_data.head(3),'\n')

    # # Download final dataset to CSV file
    # filename = 'fx_g10_intraday_' + start_date + '_' + end_date + '.csv'
    # fx_intraday_data.to_csv(TMP_DIR + filename)

    # # Print the first 3 records from the DataFrame to stdout.
    # print('Sample of fx intraday data:\n',fx_intraday_data.head(3),'\n')
