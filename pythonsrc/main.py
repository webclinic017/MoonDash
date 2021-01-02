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

### CSV Paths for Data
symbol1Path = './data/'+symbol1+'.csv'
symbol2Path = './data/'+symbol2+'.csv'

## -------------------------------------------------------------


## Functions ---------------------------------------------------

## Get Historical DataFrame
def saveSymbolsToCSV():
    """Save Data to CSV for Further Use, prevents network delay for repetitive testing
    """
    past_dataframe_symbol1 = HistoricalData.getBitmexHistoricalData(symbol1,data_count,tick_interval)
    past_dataframe_symbol2 = HistoricalData.getBitmexHistoricalData(symbol2,data_count,tick_interval)

    print('Saving Symbol 1')
    past_dataframe_symbol1.to_csv(symbol1Path,index=False)
    
    print('Saving Symbol 2')
    past_dataframe_symbol2.to_csv(symbol2Path,index=False)
    
def loadSymbolsFromCSV():
    """ Loads saved data from CSV file

    Returns:
        [pandas dataframe]: Pandas Data Frame for Symbol 1 and 2
    """
    past_dataframe_symbol1 = pd.read_csv(symbol1Path)
    past_dataframe_symbol2 = pd.read_csv(symbol2Path)
    
    return past_dataframe_symbol1,past_dataframe_symbol2


## -------------------------------------------------------------


### Load Data from CSV
past_dataframe_symbol1,past_dataframe_symbol2 = loadSymbolsFromCSV()

### Construct Main Data Frame

ticker_main = [
    past_dataframe_symbol1.close,
    past_dataframe_symbol2.close,
    past_dataframe_symbol2.close/past_dataframe_symbol1.close]

headers = [symbol1,symbol2,symbolcomposite]
ticker_main_df = pd.concat(ticker_main, axis=1, keys=headers)
ticker_main_df
