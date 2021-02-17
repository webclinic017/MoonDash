import backtrader as bt
import backtrader.feeds as btfeeds
from configs.config import inital_cash,csv_path_higherframe,csv_path_lowerframe

import pandas as pd

class Backtest:
    
    def __init__(self):
        
        self.cerebro = bt.Cerebro()

        self.cerebro.broker.setcash(inital_cash)
        print('Starting Portfolio Value: %.2f' % self.cerebro.broker.getvalue())

        self.load_data()
        
        self.cerebro.run()
        print('Final Portfolio Value: %.2f' % self.cerebro.broker.getvalue())
        
        self.cerebro.plot(style='bar')
        
    def load_data(self):
        dataframe = pd.read_csv(csv_path_higherframe,parse_dates=True,index_col=0)
        data = bt.feeds.PandasData(dataname=dataframe)
        self.cerebro.adddata(data)