import datetime
import pandas as pd
from tia.bbg import LocalTerminal 
import matplotlib.pyplot as plt
import ipdb

def down_cur_date(ticker,event,start,end):
    '''
    '''
    f = LocalTerminal.get_intraday_bar(ticker, event, start, end, interval=1).as_frame()
    #f = LocalTerminal.get_intraday_tick(ticker, event, start, end).as_frame()
    #ipdb.set_trace()
    f.set_index('time',inplace=True)
    #ipdb.set_trace()
    #if 'value' in f.columns:
    #    f = f['value']
    #else: 
    #    f = f['close']
    mean_num_event = str(int(f['numEvents'].mean()))
    f = f['close']
    f = pd.DataFrame(f)
    colstr = ticker+" "+event+ "_" + mean_num_event
    colstr = colstr.replace(" ","_")
    f.columns = [colstr]
    #f.drop_duplicates(keep='last',inplace=True)
    return f 
    # get_intraday_tick
    # events: array containing any of (TRADE, BID, ASK, BID_BEST, ASK_BEST, MID_PRICE, AT_TRADE, BEST_BID, BEST_ASK)

    # get_intraday_bar
    # events: [TRADE, BID, ASK, BID_BEST, ASK_BEST, BEST_BID, BEST_ASK]

if __name__ == '__main__':
    # starting with the g10
    curcies = ['AUD','CAD','CHF','EUR','GBP','JPY','NOK','NZD','SEK','USD']
    curncy_pair = []
    for str1 in curcies:
        for str2 in curcies:
            if str1 != str2:
                add1 = str1 + str2 + " Curncy"
                add2 = str2 + str1 + " Curncy"
                curncy_pair = curncy_pair + [add1, add2]
    
    curncy_pair = sorted(list(set(curncy_pair)))
    curncy_pair = curncy_pair[26:]

    event = ['BEST_ASK','BEST_BID']
    event = 'BEST_ASK'
    event = 'ASK_BEST'

    dt = pd.tseries.offsets.BDay(-1).apply(pd.datetime.now())
    start = pd.datetime.combine(dt-datetime.timedelta(days=365), datetime.time(13, 30))
    end = pd.datetime.combine(dt, datetime.time(14, 30))

    data_lst = []
    event_list = ['BEST_ASK','BEST_BID']
    i = 0

    for ticker in curncy_pair: 
        for event in event_list:
            data_lst.append(down_cur_date(ticker,event,start=start,end=end)) 
            i = i+1
            print("Finished with %s for %s: %i" % (ticker, event,i))
            tmpdf = pd.concat(data_lst,axis=1)
            tmpdf.to_csv('~/Desktop/fx_data_tmp.csv')

    data = pd.concat(data_lst,axis=1)
    data.to_csv('~/Desktop/fx_data_final.csv')

