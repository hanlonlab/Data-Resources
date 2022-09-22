# Download Bloomberg symbols for current members of an index 

from xbbg import blp 
import pandas as pd 

sym = "NDX Index"     # Bloomberg index 
fld = "INDX_MEMBERS"  # Field identifying members 

sym_data = blp.bds(tickers=sym,flds=fld) # pandas dataframe 

# write to file with sym_data.to_csv(filename) 
