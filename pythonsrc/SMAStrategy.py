from OrderStatus import OrderStatus
from CrossoverStatus import  CrossoverStatus

import matplotlib.pyplot as plt 

import pandas as pd
import numpy as np
import pandas_ta as ta
class SMAStrategy:
    
    ### Constructor ----------------------------------------------------------------------------------
    def __init__(self,dataframe_high,dataframe_low):
        
        ## Lower and Higher Dataframes
        self.dataframe_high = dataframe_high
        self.dataframe_low = dataframe_low
        
        ## Ema Deviation Threshold
        self.ema_dev_threshold = 5
        
        ### Current Conditions ---------------------------
        
        self.current_price = 0
        
        self.high_tf_row = dataframe_high.loc[0]
        self.stop_loss = 0   
        self.order_status = OrderStatus.NO_ORDER
        
        ## Crossover Conditions
        self.MACD_status = CrossoverStatus.NOCROSSOVER
        self.SMA_status = CrossoverStatus.NOCROSSOVER
        
        self.Previous_MACD_status = CrossoverStatus.NOCROSSOVER
        self.Previous_SMA_status = CrossoverStatus.NOCROSSOVER
    ### Constructor Ends ----------------------------------------------------------------------------------
    
    ###--------CROSSOVERS ---------------------------------------------------------------------------
    def MACDCrossOver(self,ticker_row):
        cross = False
        ## Check if Crossover has previously not occured!
        if(self.MACD_status != CrossoverStatus.CROSSOVER):    
            ## Check Cross
            if(ticker_row.MACD >= ticker_row.MACD_Signal):
                ## Both should be smaller than 0
                if(ticker_row.MACD < 0 and ticker_row.MACD_Signal <0):
                    ## Set MACD Status
                    self.Previous_MACD_status = self.MACD_status
                    self.MACD_status = CrossoverStatus.CROSSOVER
                    return True 
        return cross
        
    def MACDCrossUnder(self,ticker_row):
        cross = False
        ## Check if CrossUnder has previously not occured!
        if(self.MACD_status != CrossoverStatus.CROSSUNDER):    
            ## Check Cross
            if(ticker_row.MACD <= ticker_row.MACD_Signal):
                ## Both should be greater than 0
                if(ticker_row.MACD > 0 and ticker_row.MACD_Signal >0):
                    ## Set MACD Status
                    self.MACD_status = CrossoverStatus.CROSSUNDER
                    return True 
        return cross
        
    def SMACrossOver(self,ticker_row):
        cross = False
        ## Check if Crossover has previously not occured!
        if(self.SMA_status != CrossoverStatus.CROSSOVER):    
            ## Check Cross
            if(ticker_row.SMA_Low >= ticker_row.SMA_High):
                ## Set SMA Status
                self.SMA_status = CrossoverStatus.CROSSOVER
                return True 
        return cross
        
    def SMACrossUnder(self,ticker_row):
        cross = False
        ## Check if Crossover has previously not occured!
        if(self.SMA_status != CrossoverStatus.CROSSUNDER):    
            ## Check Cross
            if(ticker_row.SMA_Low <= ticker_row.SMA_High):
                ## Set SMA Status
                self.SMA_status = CrossoverStatus.CROSSUNDER
                return True 
        return cross
    ###--------CROSSOVER Section Complete ---------------------------------------------------------------------------
    def setHigherTFRow(self,ticker_row):
        self.high_tf_row = self.dataframe_high[
            (self.dataframe_high.timestamp <= ticker_row.timestamp)
            ].iloc[-1]
    
    def update(self,ticker_row):
        
        ## Set Current Price and Higher TF Row
        self.current_price = ticker_row.close
        self.setHigherTFRow(ticker_row)
        
        self.Previous_MACD_status = self.MACD_status
        self.Previous_SMA_status = self.SMA_status
        
        ## Check and set crossovers
        self.MACDCrossOver(ticker_row)
        self.MACDCrossUnder(ticker_row)
        
        self.SMACrossOver(ticker_row)
        self.SMACrossUnder(ticker_row)
        
        
    def set_squareOffCondition(self,ticker_row):
        
        ## Set Stop Loss ----------------------------------------
        stop_loss_delta = 4 * ticker_row.ATR
        if(self.order_status == OrderStatus.LONG):
            self.stop_loss = ticker_row.close - stop_loss_delta
        elif(self.order_status == OrderStatus.SHORT):
            self.stop_loss = ticker_row.close + stop_loss_delta
        
            
    def longOrderCondition(self,ticker_row):
        condition = False
        self.update(ticker_row)
        
        ## Check if there is no order already placed
        if(self.order_status != OrderStatus.NO_ORDER):
            condition = False
        ## If there is a CrossOver
        elif(self.MACD_status == CrossoverStatus.CROSSOVER):
            ## Check if Higher Timeframe is Trending Long
            if(self.current_price > self.high_tf_row.EMA): 
                ## EMA Deviation for Slope
                if(ticker_row.EMA_Dev > self.ema_dev_threshold):
                    ## All Conditions Satisfied, Set Long Order
                    self.order_status = OrderStatus.LONG
                    self.set_squareOffCondition(ticker_row)
                    condition = True
                    
        return condition
    
    def shortOrderCondition(self,ticker_row):
        condition = False
        return condition
    
    def updateLongSquareOff(self,ticker_row):
        if(self.SMA_status == CrossoverStatus.CROSSUNDER):
            self.set_squareOffCondition(ticker_row)
        ## On Second CrossOver
        elif(self.MACD_status == CrossoverStatus.CROSSOVER):
            if(self.Previous_MACD_status != CrossoverStatus.CROSSOVER):
                self.set_squareOffCondition(ticker_row)
                
    def longSquareOffCondition(self,ticker_row):
        condition = False
        if(self.current_price <= self.stop_loss):
            condition = True
        else:
            self.updateLongSquareOff(ticker_row)            
        return condition
            
    def shortSquareOffCondition(self,ticker_row):
        condition = False
        return condition
        
    def squareOffCondition(self,ticker_row):
        self.update(ticker_row)
        if(self.order_status == OrderStatus.LONG):
            return self.longSquareOffCondition(ticker_row)
        elif(self.order_status == OrderStatus.SHORT):
            return self.shortSquareOffCondition(ticker_row)
        else:
            return False