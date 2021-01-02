## Local Imports -----------------------------------------------
from Connections import Connections
## -------------------------------------------------------------

## Library Imports ---------------------------------------------
import pandas as pd
import numpy as np
## -------------------------------------------------------------

## Globals -----------------------------------------------------
bitmex_max_count = 1000
## -------------------------------------------------------------

class HistoricalData:
    """ A Class for getting Historical Data for different exchanges
    """
    
    def getBitmexHistoricalData(symbol,data_count,bin_size):
        """ Get Historical Data from Bitmex

        Args:
            symbol (string): Symbol String
            data_count (number): Number of Data Points to Get
            bin_size (string): Interval
        """
        
        ### Get Bitmex Client
        client = Connections.getBitmexConnection()
                
        i_lim = np.ceil(data_count/bitmex_max_count)
        print("Getting Historical Data For " + symbol)
        for i in range(int(i_lim)-1,-1,-1):
            data_start_index = bitmex_max_count*i

            past_data_list = reversed(
            client.Trade.Trade_getBucketed(
                binSize=bin_size,start=data_start_index ,count=bitmex_max_count, symbol=symbol, reverse=True
            ).result()[0])

            if(i == i_lim -1):
                past_dataframe_symbol = pd.DataFrame.from_records(past_data_list)
            else:
                past_dataframe_symbol = past_dataframe_symbol.append(
                    pd.DataFrame.from_records(past_data_list),ignore_index=True)
            
        return past_dataframe_symbol 