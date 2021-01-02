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
tick_interval = '15m'

### Symbols to run
symbol1 = 'XBTUSD'
symbol2 = 'BCHUSD'

### CSV Paths for Data
symbol1Path = './data/'+symbol1+'.csv'
symbol2Path = './data/'+symbol2+'.csv'

## -------------------------------------------------------------
class MainDataFrameKeys:
    def __init__(self,symbol1,symbol2):
        
        self.symbol1_o = self.symbol1 + '_Open'
        self.symbol1_h = self.symbol1 + '_High'
        self.symbol1_l = self.symbol1 + '_Low'
        self.symbol1_c = self.symbol1 + '_Close'
        
        self.symbol2_o = self.symbol2 + '_Open'
        self.symbol2_h = self.symbol2 + '_High'
        self.symbol2_l = self.symbol2 + '_Low'
        self.symbol2_c = self.symbol2 + '_Close'
        
        self.symbol_composite = self.symbol2+'/'+self.symbol1
        
## Functions ---------------------------------------------------
class StatisticalArbitrage:
    def __init__(self,symbol1,symbol2):
        self.symbol1 = symbol1
        self.symbol2 = symbol2
    
    ## Get Historical DataFrame
    def saveSymbolsToCSV(self,symbol1=self.symbol1,symbol2=self.symbol2,data_count,tick_interval):
        """Save Data to CSV for Further Use, prevents network delay for repetitive testing
        """
        past_dataframe_symbol1 = HistoricalData.getHistoricalData('BINANCE',symbol1,tick_interval)
        past_dataframe_symbol2 = HistoricalData.getHistoricalData('BINANCE',symbol2,tick_interval)

        HistoricalData.getBitmexHistoricalData()
        print('Saving Symbol 1')
        past_dataframe_symbol1.to_csv('./data/'+symbol1+'_'+tick_interval+'.csv',index=False)
        
        print('Saving Symbol 2')
        past_dataframe_symbol2.to_csv('./data/'+symbol2+'_'+tick_interval+'.csv',index=False)
    
    def loadSymbolsFromCSV():
        """ Loads saved data from CSV file

        Returns:
            [pandas dataframe]: Pandas Data Frame for Symbol 1 and 2
        """
        past_dataframe_symbol1 = pd.read_csv(symbol1Path)
        past_dataframe_symbol2 = pd.read_csv(symbol2Path)
        
        return past_dataframe_symbol1,past_dataframe_symbol2
    
    def getMainDataFrame(past_dataframe_symbol1,past_dataframe_symbol2):
        
        ticker_main = [
            past_dataframe_symbol1.open,
            past_dataframe_symbol1.high,
            past_dataframe_symbol1.low,
            past_dataframe_symbol1.close,
            
            past_dataframe_symbol2.open,
            past_dataframe_symbol2.high,
            past_dataframe_symbol2.low,
            past_dataframe_symbol2.close,
            
            past_dataframe_symbol2.close/past_dataframe_symbol1.close
            ]
        
        headers = [
            symbol1 + '_Open',
            symbol1 + '_High',
            symbol1 + '_Low',
            symbol1 + '_Close',
            
            symbol2 + '_Open',
            symbol2 + '_High',
            symbol2 + '_Low',
            symbol2 + '_Close',
            
            symbol2+'/'+symbol1]

        ticker_main_df = pd.concat(ticker_main, axis=1, keys=headers)
        
        return ticker_main_df


## -------------------------------------------------------------


### Load Data from CSV
# past_dataframe_symbol1,past_dataframe_symbol2 = loadSymbolsFromCSV()

# ### Construct Main Data Frame

# ticker_main = [
#     past_dataframe_symbol1.close,
#     past_dataframe_symbol2.close,
#     past_dataframe_symbol2.close/past_dataframe_symbol1.close]

# headers = [symbol1,symbol2,symbolcomposite]
# ticker_main_df = pd.concat(ticker_main, axis=1, keys=headers)
# ticker_main_df
