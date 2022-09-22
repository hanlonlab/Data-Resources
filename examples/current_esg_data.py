from xbbg import blp 
import pandas as pd 

## Granular ESG Data Download
flds = ["GHG_SCOPE_1", 
        "PCT_WOMEN_ON_BOARD",
        "COMMUNITY_SPEND_%_PRETAX_PROFIT"
        ]

# Current 
write_flag = False # option to write .csv tile to current working dir 
esgdf = blp.bdp(tickers=syms,flds=flds) 

if write_flag: 
    cwd = os.getcwd()
    flename = sym.replace(' ','_') + "_ESG_" + str(pd.Timestamp('today').date()) + '.csv'
    write_path = os.join(cwd, flename)
    esgdf.to_csv(write_path)
