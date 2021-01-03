## Local Imports -----------------------------------------------
from Connections import Connections
from OrderStatus import OrderStatus
from HistoricalData import HistoricalData
## -------------------------------------------------------------

## Library Imports ---------------------------------------------
from statsmodels.regression.rolling import RollingOLS
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
## -------------------------------------------------------------

class StatisticalArbitrageBacktest:
    
    def __init__(self,
                starting_capital,
                algo_stop_balance,
                sell_periods,
                leverage,
                transaction_fee,
                z_score_buy_threshold,
                z_score_short_threshold,
                symbol1,
                symbol2,
                ticker_main_df):
        
        self.current_balance = starting_capital
        self.balance_list = []
        
        self.order_status = OrderStatus.NO_ORDER
        self.trade_count = 0
        
        self.current_price_symbol1 =0
        self.current_price_symbol2 =0
        self.z_score = 0
        
        self.price_symbol1 = 0
        self.price_symbol2 = 0
        
        self.squareOff_price_symbol1 = 0
        self.squareOff_price_symbol2 = 0
        
        self.square_off_index = 0
        
        self.order_id_price_symbol1 =0
        self.order_id_price_symbol2 =0
        
        self.total_pnl=0
        self.total_returns=0
        self.pnl_symbol1=0
        self.returns_symbol1=0
        self.pnl_symbol2=0
        self.returns_symbol2=0
        
        self.order_details_cols = ['count',
        'order_type',
        'balance_prior',
        'balance_post',
        'total_pnl',
        'total_returns',
        'order_id_price_symbol1',
        'price_symbol1',
        'balance_alloc_symbol',
        'quantity_symbol1',
        'squareOff_price_symbol1',
        'squareOff_bal_symbol1',
        'pnl_symbol1',
        'returns_symbol1',
        'order_id_price_symbol2',
        'price_symbol2',
        'balance_alloc_symbol2',
        'quantity_symbol2',
        'squareOff_price_symbol2',
        'squareOff_bal_symbol2'
        'pnl_symbol2',
        'returns_symbol2',
        ]
        self.order_details = pd.DataFrame(data=[],columns=order_details_cols)
        
    
    def setCurrent(self):
        ## Price of 1st Asset
        self.current_price_symbol1 = row[self.symbol1 + '_Close']
        
        ## Price of 2nd Asset
        self.current_price_symbol2 = row[self.symbol2 + '_Close']
        
        ## Z Score at the moment
        self.z_score = row["Z_Score"]
        
    def OrderInit(self,index):
        ## Increment Trade Count 
        self.trade_count = self.trade_count + 1
        ## Set Square off Condition
        self.square_off_index = index + self.sell_periods
        ## Long Symbol 1 and Short Symbol 2
        self.price_symbol1 = self.current_price_symbol1
        self.price_symbol2 = self.current_price_symbol2
                
    def longOrderInit(self,index):
        ## Long Order Initialized
        self.order_status = OrderStatus.LONG
        self.OrderInit(index
               
    def shortOrderInit(self,index):
        ## Short Order Initialized
        self.order_status = OrderStatus.SHORT
        self.OrderInit(index)
        
    def generalOpenOrderCondition(self):
        if(self.order_status == OrderStatus.NO_ORDER):
            return True
        else:
            return False
            
    def generalSquareOffCondition(self):
        if(self.order_status != OrderStatus.NO_ORDER):
            return True
        else:
            return False
            
    def squareOffCondition(self,index):
        
        if(self.generalSquareOffCondition and index == self.square_off_index):
            return True
        else:
            return False
        
        
    def longOrderCondition(self):
        if(self.generalOpenOrderCondition() and self.z_score <= self.z_score_buy_threshold):
            return True
        else:
            return False
    
    def shortOrderCondition(self):
        if(self.generalOpenOrderCondition() and self.z_score <= self.z_score_buy_threshold):
            return True
        else:
            return False
            
    def orderSquareOffCalculations(self):
        
        return
            
    def longOrderSquareOff(self):
        
        return
        
    def shortOrderSquareOff(self):
        
        return
            
    def squareOffStrategy(self,index):
        if(self.order_status == OrderStatus.LONG):
            self.longOrderSquareOff()
        elif(self.order_status == OrderStatus.SHORT):
            self.shortOrderSquareOff()
            
            
    def runBacktest(self):
        
        self.setCurrent()
        
        for index,row in self.ticker_main_df.iterrows():            
            if self.current_balance > self.algo_stop_balance:
                if(self.longOrderCondition):
                    self.longOrderInit(index)
                if(self.shortOrderCondition):
                    self.shortOrderInit(index)
                if(self.squareOffCondition):
                    self.squareOffStrategy(index)
                    
                    
                
                    
                
                