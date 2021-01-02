## Local Imports -----------------------------------------------
from Connections import Connections
## -------------------------------------------------------------

## Library Imports ---------------------------------------------
from binance.client import Client
import pandas as pd
import numpy as np
import datetime
## -------------------------------------------------------------

## Globals -----------------------------------------------------
bitmex_max_count = 1000
## -------------------------------------------------------------

class HistoricalData:
    """ A Class for getting Historical Data for different exchanges
    """
    
    def getHistoricalData(exchange,symbol,data_count=1000,interval='5m',start_str='3 months ago UTC'):
        """ Get Historical Data from Bitmex

        Args:
            [symbol] (string): Symbol String,
            
            For Composite Symbols in Bitmex 
            - Read about https://www.bitmex.com/app/index/.BBCHXBT
            
            [data_count] (number): Number of Data Points to Get
            bin_size (string): Interval
        """
        
        if(exchange == 'BITMEX'):
            ### Get Bitmex Client
            client = Connections.getBitmexConnection()
                    
            i_lim = np.ceil(data_count/bitmex_max_count)
            print("Getting Historical Data For " + symbol)
            for i in range(int(i_lim)-1,-1,-1):
                data_start_index = bitmex_max_count*i

                past_data_list = reversed(
                client.Trade.Trade_getBucketed(
                    binSize=interval,start=data_start_index ,count=bitmex_max_count, symbol=symbol, reverse=True
                ).result()[0])

                if(i == i_lim -1):
                    past_dataframe_symbol = pd.DataFrame.from_records(past_data_list)
                else:
                    past_dataframe_symbol = past_dataframe_symbol.append(
                        pd.DataFrame.from_records(past_data_list),ignore_index=True)
        
        elif(exchange == 'BINANCE'):
            client = Connections.getBinanceConnection()
            klines = client.get_historical_klines(symbol,interval, start_str)
            
            past_dataframe_symbol = pd.DataFrame(data=klines,columns=[
                'timestamp',
                'open',
                'high',
                'low',
                'close',
                'volume',
                'close_time',
                'asset_volume',
                'trades',
                'buy_base_asset_volume',
                'buy_quote_asset_volume',
                'ignore'
            ])
            past_dataframe_symbol.timestamp = pd.to_datetime(past_dataframe_symbol.timestamp, unit='ms')
            
        return past_dataframe_symbol 