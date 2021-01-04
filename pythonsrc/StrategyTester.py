from HistoricalData import HistoricalData
from OrderStatus import OrderStatus
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
import pandas_ta as ta

class Backtest:
    def __init__(self,
                starting_capital,
                algo_stop_balance,
                leverage,
                transaction_fee,
                symbol,
                strategy_class,
                dataframe
                ):
        
        self.starting_capital = starting_capital 
        self.algo_stop_balance = algo_stop_balance 
        
        self.leverage = leverage 
        self.transaction_fee = transaction_fee 
        
        self.symbol = symbol
        self.current_balance = starting_capital
        
        self.balance_alloc = 0
    
        self.order_transaction_fee = 0
        
        self.squareoff_transaction_fee = 0
        
        self.quantity = 0
        self.balance_list = []
        
        
        self.current_price =0
        
        self.trade_count = 0
        self.order_status = OrderStatus.NO_ORDER
        
        self.buy_price = 0
        self.sell_price = 0
        self.pnl = 0
        
        self.square_off_index = 0
    
        self.total_pnl=0
        self.total_returns=0

        self.strategy_class = strategy_class
        self.dataframe = dataframe
        
        self.order_details_cols = [
        'count',
        'order_type',
        'balance_prior',
        'balance_post',
        'total_pnl',
        'total_returns',
        'price_symbol',
        'quantity_symbol',
        'squareOff_price_symbol',
        'order_pnl'
        ]
        self.order_details = pd.DataFrame(data=[],columns=self.order_details_cols)
        
    def setCurrent(self,row):
        ## Price of 1st Asset
        self.current_price = row.close
    
    def OrderInit(self,row,order_status):
        ## Increment Trade Count 
        self.trade_count = self.trade_count + 1
        self.order_status = order_status
        
        if(self.order_status == OrderStatus.LONG):
            self.buy_price = self.current_price
        if(self.order_status == OrderStatus.SHORT):
            self.sell_price = self.current_price
        
        ## Strategy Stop Loss Calculation
        self.strategy_class.set_stoploss(row,self.order_status)
        
    def orderTransactionFee(self,capital):
        self.order_transaction_fee = capital * self.transaction_fee
        return self.order_transaction_fee
        
    def squareOffTransactionFee(self,capital):
        self.squareoff_transaction_fee = capital * self.transaction_fee
        return self.squareoff_transaction_fee
    
    def getQuantity(self,capital,price):
        transactionFee = self.orderTransactionFee(capital)
        self.quantity = ((capital - transactionFee)/price)
        return self.quantity
    
    def getPNL(self,buyPrice,sellPrice,capital):
        transactionFee = self.squareOffTransactionFee(capital)
        self.quantity = self.getQuantity(capital,buyPrice)

        totalSP = sellPrice * quantity
        
        self.pnl = (totalSP - capital) - transactionFee
        return self.pnl
        
    def orderSquareOffCalculations(self):
        if(self.order_status == OrderStatus.LONG):
            self.sell_price = self.current_price
        if(self.order_status == OrderStatus.SHORT):
            self.buy_price = self.current_price
        
        self.balance_alloc = self.leverage * self.current_balance
        
        self.pnl = self.getPNL(self.buy_price,self.sell_price,self.balance_alloc)
        return       
    
    def squareOff(self,index):
        self.orderSquareOffCalculations()

        self.total_pnl = self.total_pnl + self.pnl
        resultant_balance = self.current_balance +  self.pnl
        
        
        self.order_details = self.order_details.append(
            pd.DataFrame(
                data=[[
                    self.trade_count,                                   
                    self.order_status,                                  
                    self.current_balance,                                   
                    resultant_balance,                                  
                    self.total_pnl,                                 
                    0,                                  
                    self.buy_price,
                    self.quantity,
                    self.sell_price,
                    self.pnl                                       
                    ]],
                columns=self.order_details_cols))
        self.current_balance = resultant_balance
        self.balance_list.append(self.current_balance)
        self.order_status = OrderStatus.NO_ORDER 
        
    def runBacktest(self):
        
        for index,row in self.dataframe.iterrows():            
            self.setCurrent(row)
            if self.current_balance > self.algo_stop_balance:
                if(self.strategy_class.longOrderCondition(row)):
                    self.OrderInit(row,OrderStatus.LONG)
                if(self.strategy_class.shortOrderCondition(row)):
                    self.OrderInit(row,OrderStatus.LONG)
                if(self.strategy_class.squareOffCondition(row)):
                    self.squareOff(index)
        
        return self.current_balance,self.balance_list,self.order_details
    