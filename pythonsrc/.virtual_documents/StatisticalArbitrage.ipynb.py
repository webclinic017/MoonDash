# get_ipython().run_line_magic("matplotlib", " notebook")
from StatisticalArbitrage import StatisticalArbitrage as sta
from StatisticalArbitrageBacktest import StatisticalArbitrageBacktest as stab
from OrderStatus import OrderStatus
import matplotlib.pyplot as plt
import time, requests, json
from decouple import config
import pandas as pd
import numpy as np
import bitmex



symbol1 = 'BTCUSDT'
symbol2 = 'BCHUSDT'

tick_interval = '1m'
tick_interval_small = '5m'

### CSV Paths for Data
symbol1Path = './data/'+symbol1+'_'+tick_interval+'.csv'
symbol2Path = './data/'+symbol2+'_'+tick_interval+'.csv'

symbol1Path_small = './data/'+symbol1+'_'+tick_interval_small+'.csv'
symbol2Path_small = './data/'+symbol2+'_'+tick_interval_small+'.csv'

symbolcomposite = '.BBCHXBT'

data_count = 20000
bitmex_max_count = 1000

current_balance = starting_capital = 10000
algo_stop_balance = 0.1 * starting_capital

rolling_window = 75
sell_periods = 1

z_score_buy_threshold = -3
z_score_short_threshold = 3

transaction_fee = 0.05/100

leverage = 20


# sta.saveSymbolsToCSV(symbol1,symbol2,tick_interval)
# sta.saveSymbolsToCSV(symbol1,symbol2,tick_interval_small)

past_dataframe_symbol1,past_dataframe_symbol2 = sta.loadSymbolsFromCSV(symbol1Path,symbol2Path)
ticker_main_df = sta.getMainDataFrame(symbol1,symbol2,past_dataframe_symbol1,past_dataframe_symbol2)






ticker_main_df = sta.zScoreDF(ticker_main_df,rolling_window,symbol1,symbol2)
sta.plotZScore(ticker_main_df,z_score_buy_threshold,z_score_short_threshold)



 back = stab(starting_capital,
                        algo_stop_balance,
                        sell_periods,
                        leverage,
                        transaction_fee,
                        z_score_buy_threshold,
                        z_score_short_threshold,
                        symbol1,symbol2,ticker_main_df)      
current_balance,balance_list,order_details = back.runBacktest()
cap_returns = round((current_balance -starting_capital) *100/current_balance)

fig = plt.figure()
plt.plot(balance_list)
plt.show()


print(cap_returns)


order_details


order_details.to_csv('./data/OrderDetails.csv',index=False)
