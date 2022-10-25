import pandas as pd
from tia.bbg import LocalTerminal
import numpy as np

if __name__ == "__main__": 
    #stkdf = pd.read_csv('stks.csv')
    #optdf = pd.read_csv('opts.csv')
    
    #stktkrs = list(stkdf.iloc[2:-1]['Symbol'])
    #bbgstks = [st + " US Equity" for st in stktkrs]
    
    bbgstks = ["AGG US Equity"]#,"DAX Index"] 
    
    
    stkprc = LocalTerminal.get_reference_data(bbgstks,'PX_LAST')

    allopttkrs = []
    
    for stk in bbgstks:
        lastprc = float(stkprc.as_frame().loc[stk,:].values)
        optchain = LocalTerminal.get_reference_data(stk,'OPT_CHAIN')
        opttkrs = list(optchain.as_frame().values)
        optrkrs1 = optchain.as_frame()['OPT_CHAIN'].values.flatten()[0].values.flatten()
        optrkrs1 = list(optrkrs1)
	
        reftkrs = []
        maxdays = 140
        permoney = 0.3 
        lowstk = lastprc*(1-permoney)
        highstk = lastprc*(1+permoney)
	
    
        for tkr in optrkrs1:
            import pdb 
            print tkr
            dayexpir = pd.to_datetime(tkr.split(' ')[2])-pd.to_datetime('today')
            stk = float(tkr.split(' ')[-2][1:])
            stkcnd = (stk > lowstk) and (stk < highstk)        
            if int(dayexpir.days) < maxdays and stkcnd:
                reftkrs.append(tkr)
        allopttkrs.append(np.array(reftkrs))     
	
    fintkrs = list(np.array(allopttkrs).flatten())
    fintkrs = map(list,fintkrs)
    fintkrs = [item for sublist in fintkrs for item in sublist]
    fintkrs = bbgstks + fintkrs
    
    start = '01/26/2019'
    end = '12/01/2021'

    biddata = LocalTerminal.get_historical(fintkrs,'PX_BID',start=start,end=end)
    askdata = LocalTerminal.get_historical(fintkrs,'PX_ASK',start=start,end=end)
    volata = LocalTerminal.get_historical(fintkrs,'PX_VOLUME',start=start,end=end)
	
    biddata.as_frame().to_csv('biddata.csv')
    askdata.as_frame().to_csv('askdata.csv')
    volata.as_frame().to_csv('volume.csv')