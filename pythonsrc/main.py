## Local Imports -----------------------------------------------
from Connections import Connections
from HistoricalData import HistoricalData
## -------------------------------------------------------------

## Library Imports ---------------------------------------------
import pandas as pd
import numpy as np
## -------------------------------------------------------------

## Globals -----------------------------------------------------

### Data Count For Testing
data_count = 17280      #60 days = 86400 mins =  17280 * 5 min intervals
tick_interval = '5m'

### Symbols to run
symbol1 = 'XBTUSD'
symbol2 = 'BCHUSD'

## -------------------------------------------------------------


## Get Historical DataFrame
def saveSymbolsToCSV():
    past_dataframe_symbol1 = HistoricalData.getBitmexHistoricalData(symbol1,data_count,tick_interval)
    past_dataframe_symbol2 = HistoricalData.getBitmexHistoricalData(symbol2,data_count,tick_interval)

    print('Saving Symbol 1')
    past_dataframe_symbol1.to_csv('./data/'+symbol1+'.csv',index=False)
    
    print('Saving Symbol 2')
    past_dataframe_symbol2.to_csv('./data/'+symbol2+'.csv',index=False)