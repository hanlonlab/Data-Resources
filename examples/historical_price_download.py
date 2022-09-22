from xbbg import blp 
import pandas as pd 
import os 

# Download historical last price and market cap

write_flag = False # option to write .csv tile to current working dir 
start_date = '2010-01-01'
end_date = '2022-09-01'
flds = ['PX_LAST','CUR_MKT_CAP']  # data fields 
syms = ['IBM US Equity','GOOG US Equity'] # bloomberg tickers 

prcdf = blp.bdh(tickers=syms,flds=flds,start_date=start_date,end_date=end_date) 

if write_flag: 
    cwd = os.getcwd()
    flename = sym.replace(' ','_') + "_Price_" + start_date + '_' +  end_date + '.csv'              
    write_path = os.join(cwd, flename)
    prcdf.to_csv(write_path)
