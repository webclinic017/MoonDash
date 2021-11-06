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
        if(self.order_status != OrderStatus.NO_ORDER):
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
        