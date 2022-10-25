import kaiko 
import datetime as dt 
import pandas as pd 

# github repo
# https://github.com/sgheb/kaiko-api/tree/master/kaiko

# Setting a client with your API key

API_KEY = 'some-api-key'

kc = kaiko.KaikoClient(api_key=API_KEY)

# Getting some simple daily candles
ds = kaiko.OrderBookAggregations(type_of_aggregate = 'OHLCV', exchange = 'lmax', instrument = 'btc-usd', start_time='2022-08-01', interval='1d', client=kc)

# Retrieve the dataframe containing the data
data = ds.df


exchanges_list = ['cbse', 'ftxx','krkn'] # coinbase, ftx, kracken to start 

currencys = ['btc','eth','usd'] 

pairs = [] 
for cur1 in currencys: 
    for cur2 in currencys: 
        if cur1 != cur2: 
           tmppair = cur1 + '-' + cur2
           pairs.append(tmppair) 

# instrument --------------------------------------
pair = 'btc-usd'

# 30 days ago --------------------------------------
N = 1
d = dt.timedelta(days=N)
today = pd.Timestamp('today') 
start = today - d
# from datetime to string 
start = start.strftime('%Y-%m-%d %H')

# interval (1m, 10m, 1h, 1d etc.) -------------------
interv = '1s' #1d, 1m, or 1s for example at 1d, 1m, and 1s aggregates 

for exh in exchanges_list: 
    for inst in pairs: 
        inst = 'btc-usd'
        #ds = kaiko.OrderBookAggregations(type_of_aggregate = 'COHLCV', exchange = exh,
        #instrument = inst , start_time = start, interval = interv, client = kc)
        ds = kaiko.Candles(type_of_aggregate = 'COHLCV', exchange = exh,
        instrument = inst , start_time = start, interval = interv, client = kc)
        #ds = kaiko.TickTrades(exchange = exh,
        #instrument = inst , start_time = start, interval = interv, client = kc)
        #ds = kaiko.OrderBookSnapshots(exchange = exh,
        #instrument = inst , start_time = start, interval = interv, client = kc)

        data = ds.df

        import ipdb 
        ipdb.set_trace() 
