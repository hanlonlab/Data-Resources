#!/usr/bin/env python3
# coding: utf-8

import requests
import json
import os
import sys

import subprocess
import sqlite3
import datetime
import re

"""
Below we grab the Kaiko API key from .kaikopass file in user home directory.

API key permits the following access:
Data types -> All (Trades, Order Books, OHLCV/VWAP Aggregates)
Endpoints Access -> All
Exchanges/Pairs -> All
Delivery -> Rest API

Other info:
API Documentation -> https://docs.kaiko.com/#introduction
Data Dictionary -> https://www.kaiko.com/pages/cryptocurrency-data-types
Kaiko-maintained Python API -> https://github.com/sgheb/kaiko-api
"""

# TODO assert CRED_PATH is 644, same as .pgpass does
HOME_PATH = os.path.expanduser('~')
CRED_PATH = HOME_PATH + '/.kaikopass'  # api credentials stored as string in format "kaikoapi:apikey"
with open(CRED_PATH, 'r') as f:
    valid_creds = [line for line in f if line.startswith('kaiko')][0].split(':')
    API_KEY = valid_creds[1].rstrip('\n')

# set up global vars
TMP_DIR = '../tmp/'
MKT_API_CONFIG = {
    'base_url': 'https://us.market-api.kaiko.io/',
    'version': 'v2',
    'headers': {'Accept': 'application/json','X-Api-Key': API_KEY}
}
REF_API_CONFIG = {
    'base_url': 'https://reference-data-api.kaiko.io/',
    'version': 'v1',
    'headers': {'Accept': 'application/json'}
}
VALID_REFERENCE_TYPES = ['assets','exchanges','instruments','pools']
VALID_MKT_DATA_TYPES = ['trades','ohlcv']
VALID_ARG_LENS = {
    'new': [3],
    'list': [3,4]
}

# get request information from kaiko config file
KAIKO_CONFIG_PATH = './config/kaiko.conf'
with open(KAIKO_CONFIG_PATH) as file:
    kaiko_config = json.load(file)

def new_mkt_data_request(mkt_data_type: str, ref_cols: bool = True) -> int:
    r"""
    Send a new request to the Kaiko Market Data API

    :return: 0 on success
    """

    params = kaiko_config[mkt_data_type]
    if mkt_data_type='trades':
        get_url = MKT_API_CONFIG['base_url'] + MKT_API_CONFIG['version'] + '/data/{commodity}.{data_version}/exchanges/{exchange}/{instrument_class}/{instrument}/{request_type}?start_time={start_time}&end_time={end_time}&page_size={page_size}'.format(**params)
    elif mkt_data_type='ohlcv':
        get_url = MKT_API_CONFIG['base_url'] + MKT_API_CONFIG['version'] + '/data/{commodity}.{data_version}/exchanges/{exchange}/{instrument_class}/{instrument}/{request_type}?start_time={start_time}&end_time={end_time}&page_size={page_size}&interval={interval}'.format(**params)

    with requests.Session() as s:
        # authenicate to api, get token
        r = s.request(method='GET', url=get_url, headers=MKT_API_CONFIG['headers'])

        # set filename for downloaded data
        export_path = TMP_DIR + mkt_data_type + '_{exchange}_{instrument_class}_{instrument}_{start_time}_{end_time}.csv'.format(**params).replace(':','')

        # download data
        response = json.loads(r.content)
        ref_headers = 'commodity,exchange,instrument_class,instrument,'.format(**params)
        ref_data = '{commodity},{exchange},{instrument_class},{instrument},'.format(**params)

        # write first page
        if ref_cols:
            with open(export_path, 'w') as file:
                file.write(ref_headers + ','.join(list(response['data'][0].keys())) + '\n')
                for record in response['data']:
                    file.write(ref_data + ','.join([str(val) for val in record.values()]) + '\n')
        else:
            with open(export_path, 'w') as file:
                file.write(','.join(list(response['data'][0].keys())) + '\n')
                for record in response['data']:
                    file.write(','.join([str(val) for val in record.values()]) + '\n')

        # write subsequent pages
        while 'next_url' in response:
            r = s.request(method='GET', url=response['next_url'], headers=MKT_API_CONFIG['headers'])
            response = json.loads(r.content)
            if ref_cols:
                with open(export_path, 'a') as file:
                    for record in response['data']:
                        file.write(ref_data + ','.join([str(val) for val in record.values()]) + '\n')
            else:
                with open(export_path, 'a') as file:
                    for record in response['data']:
                        file.write(','.join([str(val) for val in record.values()]) + '\n')

    return 0


def new_ref_data_request(request_type: str, query_filter: str = '') -> int:
    r"""
    Send a new request to the Kaiko Reference Data API. See https://docs.kaiko.com/#reference-data-api

    :param request_type: Type of reference data to request
    :type request_type: str
    :return: 0 on success
    """

    get_url = REF_API_CONFIG['base_url'] + REF_API_CONFIG['version'] + '/' + request_type + query_filter

    with requests.Session() as s:
        # authenicate to api, get token
        r = s.request(method='GET', url=get_url, headers=REF_API_CONFIG['headers'])

        # compose report request body, pull all fields from field list
        print('Status code: ', r.status_code, '\n\nContent:\n', json.dumps(json.loads(r.content), indent=4), '\n\n')
        # for item in json.loads(r.content)['value']:
        #     pass()

    return 0


def usage():
    r"""
    Print a descriptive usage message
    """

    msg = """usage: {0} func opt [query]
    func: "new" for market data, "list" for metadata
    opt:
        if func is new: type of market data to request, one of {1}
        if func is list: type of metadata to request, one of {2}
    query:
        if func is new: omit
        if func is list: query string in the form \?param=val&param=val - more info at https://docs.kaiko.com/#parameters-3""".format(
            sys.argv[0],
            '|'.join(VALID_MKT_DATA_TYPES),
            '|'.join(VALID_REFERENCE_TYPES)
            )

    sys.exit(msg)


if __name__ == "__main__":

    if sys.argv[1] == 'new' and len(sys.argv) in VALID_ARG_LENS['new']:
        new_mkt_data_request(sys.argv[2])
    elif sys.argv[1] == 'list'  and len(sys.argv) in VALID_ARG_LENS['list'] and sys.argv[2] in VALID_REFERENCE_TYPES:
        if len(sys.argv) >= 4:
            new_ref_data_request(sys.argv[2], sys.argv[3])
        else:
            new_ref_data_request(sys.argv[2])
    else:
        usage()
