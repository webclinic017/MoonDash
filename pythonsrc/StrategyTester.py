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
        
        self.open_time = None
        self.close_time = None
        
        self.close_reason = ''
        
        
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
        'open_time',
        'close_time',
        'order_type',
        'balance_prior',
        'balance_post',
        'total_pnl',
        'price_symbol',
        'quantity_symbol',
        'squareOff_price_symbol',
        'order_pnl',
        'pnl_percentage'
        ]
        self.order_details = pd.DataFrame(data=[],columns=self.order_details_cols)
        
    def setCurrent(self,row):
        ## Price of 1st Asset
        self.current_price = row.close
    
    def OrderInit(self,row,order_status):
        ## Increment Trade Count 
        
        self.trade_count = self.trade_count + 1
        self.order_status = order_status
        self.open_time = row.timestamp
        
        if(self.order_status == OrderStatus.LONG):
            self.buy_price = self.current_price
        if(self.order_status == OrderStatus.SHORT):
            self.sell_price = self.current_price
        
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

        totalSP = sellPrice * self.quantity
        
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
    
    def squareOff(self,row,index):
        self.orderSquareOffCalculations()
        self.close_time = row.timestamp
        self.total_pnl = self.total_pnl + self.pnl
        resultant_balance = self.current_balance +  self.pnl
        pnl_percentage = round((self.pnl * 100)/self.current_balance)
        
        self.order_details = self.order_details.append(
            pd.DataFrame(
                data=[[
                    self.trade_count,
                    self.open_time,
                    self.close_time,
                    self.order_status,                                  
                    self.current_balance,                                   
                    resultant_balance,                                  
                    self.total_pnl,                                                               
                    self.buy_price,
                    self.quantity,
                    self.sell_price,
                    self.pnl,
                    pnl_percentage
                    ]],
                columns=self.order_details_cols),ignore_index=True)
        self.current_balance = resultant_balance
        self.balance_list.append(self.current_balance)
        self.strategy_class.order_status = OrderStatus.NO_ORDER
        self.order_status = OrderStatus.NO_ORDER 
       
       
    def summarize(self):
        
        cap_returns = ((self.current_balance - self.starting_capital) *100/self.starting_capital)
        
        max_loss = self.order_details.pnl_percentage.min()
        max_profit = self.order_details.pnl_percentage.max()
        
        total_trades = self.order_details.shape[0]
        
        n_loss_trades = self.order_details[(self.order_details.pnl_percentage < 0)].shape[0]
        n_profit_trades = self.order_details[(self.order_details.pnl_percentage > 0)].shape[0]
        
        profit_trades_percentage = round((n_profit_trades * 100)/total_trades)
        
        summary  =  pd.DataFrame(data={
            "cap_returns" : cap_returns,
            "max_loss" : max_loss,
            "max_profit" : max_profit,
            "total_trades":total_trades,
            "n_loss_trades":n_loss_trades,
            "n_profit_trades":n_profit_trades,
            "profit_trades_percentage":profit_trades_percentage,
        })
    def runBacktest(self):
        
        for index,row in self.dataframe.iterrows():            
            self.setCurrent(row)
            if self.current_balance > self.algo_stop_balance:
                if(self.strategy_class.longOrderCondition(row)):
                    self.OrderInit(row,OrderStatus.LONG)
                if(self.strategy_class.shortOrderCondition(row)):
                    self.OrderInit(row,OrderStatus.SHORT)
                if(self.strategy_class.squareOffCondition(row)):
                    self.squareOff(row,index)
        
        
        
        return self.current_balance,self.balance_list,self.order_details