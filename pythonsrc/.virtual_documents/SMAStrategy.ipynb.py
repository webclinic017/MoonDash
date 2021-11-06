# get_ipython().run_line_magic("matplotlib", " inline")
# import mpld3
# mpld3.enable_notebook()

from HistoricalData import HistoricalData
from OrderStatus import OrderStatus

import matplotlib.pyplot as plt 

import mplfinance as fplt

import matplotlib.dates as mpl_dates

import pandas as pd
import numpy as np
import pandas_ta as ta




def saveDataToCSV(symbol,timeframe='5m',higher_timeframe='30m',start_str='1 year ago UTC'):
    timeframe_pastData = HistoricalData.getHistoricalData('BINANCE',symbol,interval=timeframe,
                                                         start_str=start_str)
    
    path1 = './data/SMA/'+symbol+'_'+timeframe+'.csv'
    print("Saving Data to "+path1)
    
    timeframe_pastData.to_csv(path1,index=False)
    
    highertimeframe_pastData = HistoricalData.getHistoricalData('BINANCE',symbol,interval=higher_timeframe,
                                                         start_str=start_str)
    
    path2 = './data/SMA/'+symbol+'_'+higher_timeframe+'.csv'
    print("Saving Data to "+path2)
    
    highertimeframe_pastData.to_csv(path2,index=False)


symbol = 'BTCUSDT'

timeframe='5m'
higher_timeframe='30m'

lower_sma_interval = 22
higher_sma_interval = 55

sma_macd_interval = 13

atr_len = 10
filter_ma_interval = 200

path1 = './data/SMA/'+symbol+'_'+timeframe+'.csv'
path2 = './data/SMA/'+symbol+'_'+higher_timeframe+'.csv'
# saveDataToCSV(symbol)


dataframe_low = pd.read_csv(path1)
dataframe_high = pd.read_csv(path2)


dataframe_low.head(1)


dataframe_high.tail(1)


startTimeStamp = dataframe_high.head(1).timestamp.item()
endTimeStamp = dataframe_high.tail(1).timestamp.item()


dataframe_low = dataframe_low[(dataframe_low.timestamp>=startTimeStamp) 
                              & (endTimeStamp>=dataframe_low.timestamp)]
dataframe_low = dataframe_low.reset_index(drop=True)


dataframe_low['SMA_Low'] = ta.sma(dataframe_low.close,length=lower_sma_interval)
dataframe_low['SMA_High'] = ta.sma(dataframe_low.close,length=higher_sma_interval)

ohlc_dataframe_low = ta.ohlc4(dataframe_low.open,dataframe_low.high,
                             dataframe_low.low,dataframe_low.close)

dataframe_low['MACD_EMA_Low'] = ta.ema(ohlc_dataframe_low,length=lower_sma_interval)
dataframe_low['MACD_EMA_High'] = ta.ema(ohlc_dataframe_low,length=higher_sma_interval)

dataframe_low['MACD'] = dataframe_low['MACD_EMA_High'] - dataframe_low['MACD_EMA_Low']

dataframe_low['MACD_Signal'] = ta.sma(dataframe_low.MACD,length=sma_macd_interval)

dataframe_low['EMA'] = ta.ema(ohlc_dataframe_low,length=filter_ma_interval)
dataframe_low['ATR'] = ta.atr(dataframe_low.high, dataframe_low.low, dataframe_low.close, length=atr_len)
dataframe_low['EMA_Dev'] = dataframe_low.EMA.rolling(22).std()

dataframe_low = dataframe_low.dropna().reset_index(drop=True)



dataframe_low


dataframe_high['SMA_Low'] = ta.sma(dataframe_high.close,length=lower_sma_interval)
dataframe_high['SMA_High'] = ta.sma(dataframe_high.close,length=higher_sma_interval)
ohlc_dataframe_high = ta.ohlc4(dataframe_high.open,dataframe_high.high,
                             dataframe_high.low,dataframe_high.close)

dataframe_high['MACD_EMA_Low'] = ta.ema(ohlc_dataframe_high,length=lower_sma_interval)
dataframe_high['MACD_EMA_High'] = ta.ema(ohlc_dataframe_high,length=higher_sma_interval)

dataframe_high['MACD'] = dataframe_high['MACD_EMA_High'] - dataframe_high['MACD_EMA_Low']

dataframe_high['MACD_Signal'] = ta.sma(dataframe_high.MACD,length=sma_macd_interval)
dataframe_high['EMA'] = ta.ema(ohlc_dataframe_high,length=filter_ma_interval)
dataframe_high['ATR'] = ta.atr(dataframe_high.high, dataframe_high.low, dataframe_high.close, length=atr_len)
dataframe_high['EMA_Dev'] = dataframe_high.EMA.rolling(22).std()

dataframe_high = dataframe_high.dropna().reset_index(drop=True)


dataframe_low


dataframe_high


fig = plt.figure()
plt.plot(dataframe_low.SMA_Low[0:500])
plt.plot(dataframe_low.SMA_High[0:500])
plt.plot(dataframe_low.EMA[0:500])
plt.show()


startTimeStamp = dataframe_high.head(1).timestamp.item()
endTimeStamp = dataframe_high.tail(1).timestamp.item()
startTimeStamp,endTimeStamp
dataframe_low = dataframe_low[(dataframe_low.timestamp>=startTimeStamp) 
                              & (endTimeStamp>=dataframe_low.timestamp)]
dataframe_low = dataframe_low.reset_index(drop=True)
dataframe_low


dataframe_high



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
        'trade_duration',
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
        
        trade_duration = pd.to_datetime(self.close_time) - pd.to_datetime(self.open_time)
        
        self.order_details = self.order_details.append(
            pd.DataFrame(
                data=[[
                    self.trade_count,
                    self.open_time,
                    self.close_time,
                    trade_duration,
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
        
        tested_from = self.dataframe.iloc[0].timestamp
        tested_to = self.dataframe.iloc[-1].timestamp
        
        test_duration = pd.to_datetime(tested_to) - pd.to_datetime(tested_from)
        
        average_trade_duration = (self.order_details.trade_duration).mean()
        
        cap_returns = ((self.current_balance - self.starting_capital) *100/self.starting_capital)
        
        max_loss = self.order_details.pnl_percentage.min()
        max_profit = self.order_details.pnl_percentage.max()
        
        total_trades = self.order_details.shape[0]
        
    
        loss_trades = self.order_details[(self.order_details.pnl_percentage < 0)]
        profit_trades = self.order_details[(self.order_details.pnl_percentage > 0)]
        
        average_pnl_trade = self.order_details.pnl_percentage.mean()
        average_pnl_loss_trades = loss_trades.pnl_percentage.mean()
        average_pnl_profit_trades = profit_trades.pnl_percentage.mean()
        
        n_loss_trades = loss_trades.shape[0]
        n_profit_trades = profit_trades.shape[0]
        
        profit_trades_percentage = round((n_profit_trades * 100)/total_trades)
        
        
        
        summary  =  pd.DataFrame(data={
            "tested_from" :tested_from,
            "tested_to":tested_to,
            "test_duration":test_duration,
            "average_trade_duration":average_trade_duration,
            "cap_returns" : cap_returns,
            "max_loss" : max_loss,
            "max_profit" : max_profit,
            "total_trades":total_trades,
            "n_loss_trades":n_loss_trades,
            "n_profit_trades":n_profit_trades,
            "profit_trades_percentage":profit_trades_percentage,
            "average_pnl_trade":average_pnl_trade,
            "average_pnl_loss_trades":average_pnl_loss_trades,
            "average_pnl_profit_trades":average_pnl_profit_trades
        },index=[0])
        
        return summary
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
        
        summary = self.summarize()
        print(summary.iloc[0])
        
        return self.current_balance,self.balance_list,self.order_details



class SMAStrategy:
    def __init__(self,dataframe_high,dataframe_low):
        self.dataframe_high = dataframe_high
        self.dataframe_low = dataframe_low
        
        self.ema_dev_threshold = 5
        
        self.stop_loss = 0
        self.high_tf_row = dataframe_high.loc[0]
        
        self.order_status = OrderStatus.NO_ORDER
        self.crossunder = 0
        self.crossover = 0
    
    def crossOver(self,ticker_row):
        if(ticker_row.MACD >= ticker_row.MACD_Signal):
        #         if(ticker_row.SMA_Low >= ticker_row.SMA_High):
            self.crossover = 1
            self.crossunder = 0
            return True
        else:
            return False
    def crossUnder(self,ticker_row):
        if(ticker_row.SMA_Low <= ticker_row.SMA_High):
            self.crossunder = 1
            self.crossover = 0
            return True
        else:
            return False
        
    def set_squareOffCondition(self,ticker_row):
        
        #stop_loss_delta = (ticker_row.close * 0.02) + ticker_row.ATR
        stop_loss_delta = 4 * ticker_row.ATR
        if(self.order_status == OrderStatus.LONG):
            self.stop_loss = ticker_row.close - stop_loss_delta
        elif(self.order_status == OrderStatus.SHORT):
            self.stop_loss = ticker_row.close + stop_loss_delta
        
            
    def longOrderCondition(self,ticker_row):
        condition = False
        current_price = ticker_row.close
        if(self.order_status get_ipython().getoutput("= OrderStatus.NO_ORDER):")
            condition = False
        elif(self.crossOver(ticker_row)):
            self.high_tf_row = self.dataframe_high[
                (self.dataframe_high.timestamp <= ticker_row.timestamp)
            ].iloc[-1]
            
            if((current_price > self.high_tf_row.EMA) 
              and 
               (ticker_row.EMA_Dev >self.ema_dev_threshold)
              ):
                self.order_status = OrderStatus.LONG
                self.set_squareOffCondition(ticker_row)
                condition = True
        
        return condition
    
    def shortOrderCondition(self,ticker_row):
        return False
    
    def longSquareOffCondition(self,ticker_row):
        current_price = ticker_row.close
        condition = False
        if(current_price <= self.stop_loss):
            self.crossover = 0
            self.crossunder = 0
            condition = True
        elif(self.crossunder == 0):
            if(self.crossUnder(ticker_row)):
                self.set_squareOffCondition(ticker_row)
        elif(self.crossover == 0):
            if(self.crossOver(ticker_row)):
                self.set_squareOffCondition(ticker_row)
        
        return condition
            
    def shortSquareOffCondition(self,ticker_row):
        current_price = ticker_row.close
        if(current_price >= self.stop_loss):
            return True
#         else:
#             return self.crossOver(ticker_row)
        
    def squareOffCondition(self,ticker_row):
        
        if(self.order_status == OrderStatus.LONG):
            return self.longSquareOffCondition(ticker_row)
        elif(self.order_status == OrderStatus.SHORT):
            return self.shortSquareOffCondition(ticker_row)
        else:
            return False
        


sma_strategy = SMAStrategy(dataframe_high,dataframe_low)

back = Backtest(
    10000,
    1000,
    3,
    0.075/100,
    'BTCUSDT',
    sma_strategy,
    dataframe_low)
current_balance,balance_list,order_details = back.runBacktest()
# cap_returns = round((current_balance -starting_capital) *100/current_balance)

fig = plt.figure()
# plt.plot(dataframe_low.loc[0:10000].close)
plt.plot(balance_list)
plt.show()
order_details
order_details.to_csv('./data/SMA/OrderDetails.csv',index=False)
# balance_list


cap_returns = ((current_balance -10000) *100/10000)
cap_returns


order_details.iloc[0].close_time


len_p = 1000
fig = plt.figure(figsize=(16,8))
# plt.plot(dataframe_low.SMA_Low[0:len_p])
# plt.plot(dataframe_low.SMA_High[0:len_p])
# plt.plot(dataframe_low.EMA[0:len_p])

plt.plot(dataframe_low.MACD[0:len_p])
plt.plot(dataframe_low.MACD_Signal[0:len_p])
plt.show()


plt.plot(dataframe_low.EMA_Dev[0:len_p])


max_loss = order_details.pnl_percentage.min()
max_profit = order_details.pnl_percentage.max()


plt.figure(figsize=(16,8))
plt.axhline(0,c="black")
# plt.axhline(max_loss,c="salmon")
# plt.axhline(max_profit,c="salmon")
# plt.text(y=max_loss, x=0, s=('Max Loss : ' + str(max_loss)))
# plt.text(y=max_profit, x=0, s=('Max Profit : ' + str(max_profit)))
plt.plot(order_details.pnl_percentage)
plt.stem(order_details.pnl_percentage,use_line_collection=True)


order_details[(order_details.pnl_percentage < 0)].shape[0]


order_details[(order_details.pnl_percentage > 0)].shape[0]


df = dataframe_low
df['timestamp'] = pd.to_datetime(df.timestamp)
df  = df.set_index('timestamp')

df
# plt.figure(figsize = (16,8))
# plt.plot(dataframe_low.close)
