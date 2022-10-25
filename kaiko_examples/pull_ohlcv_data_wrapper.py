#!/usr/bin/env python3
# coding: utf-8

import kaiko
import json
import os

# TODO assert CRED_PATH is 644, same as .pgpass does
HOME_PATH = os.path.expanduser('~')
CRED_PATH = HOME_PATH + '/.kaikopass'  # api credentials stored as string in format "kaikoapi:apikey"
with open(CRED_PATH, 'r') as f:
    valid_creds = [line for line in f if line.startswith('kaiko')][0].split(':')
    API_KEY = valid_creds[1].rstrip('\n')

# set up global vars
TMP_DIR = '../tmp/'

# get request information from kaiko config file
KAIKO_CONFIG_PATH = './config/kaiko.conf'
with open(KAIKO_CONFIG_PATH) as file:
    kaiko_config = json.load(file)


if __name__ == "__main__":

    # instantiate Kaiko client
    client = kaiko.KaikoClient(api_key=API_KEY)

    # get OHLCV request config dict from kaiko config dict
    ohlcv_config = kaiko_config['ohlcv']

    # get the OHLCV data
    datastore = kaiko.OrderBookAggregations(
        client=client,
        type_of_aggregate = 'COHLCV',
        exchange = ohlcv_config['exchange'],
        instrument = ohlcv_config['instrument'],
        start_time=ohlcv_config['start_time'],
        interval=ohlcv_config['interval']
    )
    
    # save the dataframe to CSV file
    datastore.df.to_csv(TMP_DIR + 'ohlcv_kaiko_example.csv')

    # print first five records from the dataframe
    print('Top of dataframe containing results:\n',datastore.df.head(5))
