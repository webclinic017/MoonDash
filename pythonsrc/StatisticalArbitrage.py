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

## -------------------------------------------------------------
class MainDataFrameKeys:
    def __init__(self,symbol1,symbol2):
        
        self.symbol1_o = self.symbol1 + '_Open'
        self.symbol1_h = self.symbol1 + '_High'
        self.symbol1_l = self.symbol1 + '_Low'
        self.symbol1_c = self.symbol1 + '_Close'
        
        self.symbol2_o = self.symbol2 + '_Open'
        self.symbol2_h = self.symbol2 + '_High'
        self.symbol2_l = self.symbol2 + '_Low'
        self.symbol2_c = self.symbol2 + '_Close'
        
        self.symbol_composite = self.symbol2+'/'+self.symbol1
        
## Functions ---------------------------------------------------
class StatisticalArbitrage:
    def __init__(self,symbol1,symbol2):
        self.symbol1 = symbol1
        self.symbol2 = symbol2
    
    ## Get Historical DataFrame
    def saveSymbolsToCSV(symbol1,symbol2,tick_interval):
        """Save Data to CSV for Further Use, prevents network delay for repetitive testing
        """
        past_dataframe_symbol1 = HistoricalData.getHistoricalData('BINANCE',symbol=symbol1,interval=tick_interval)
        past_dataframe_symbol2 = HistoricalData.getHistoricalData('BINANCE',symbol=symbol2,interval=tick_interval)

        print('Saving Symbol 1')
        symbol1_path = './data/'+symbol1+'_'+tick_interval+'.csv'
        past_dataframe_symbol1.to_csv(symbol1_path,index=False)
        
        print('Saving Symbol 2')
        symbol2_path = './data/'+symbol2+'_'+tick_interval+'.csv'
        past_dataframe_symbol2.to_csv(symbol2_path,index=False)
        
        return symbol1_path,symbol2_path
        
    
    def loadSymbolsFromCSV(symbol1Path,symbol2Path):
        """ Loads saved data from CSV file

        Returns:
            [pandas dataframe]: Pandas Data Frame for Symbol 1 and 2
        """
        past_dataframe_symbol1 = pd.read_csv(symbol1Path)
        past_dataframe_symbol2 = pd.read_csv(symbol2Path)
        
        return past_dataframe_symbol1,past_dataframe_symbol2
    
    def getMainDataFrame(symbol1,symbol2,past_dataframe_symbol1,past_dataframe_symbol2):
        
        ticker_main = [
            past_dataframe_symbol1.open,
            past_dataframe_symbol1.high,
            past_dataframe_symbol1.low,
            past_dataframe_symbol1.close,
            
            past_dataframe_symbol2.open,
            past_dataframe_symbol2.high,
            past_dataframe_symbol2.low,
            past_dataframe_symbol2.close,
            
            past_dataframe_symbol2.close/past_dataframe_symbol1.close
            ]
        
        headers = [
            symbol1 + '_Open',
            symbol1 + '_High',
            symbol1 + '_Low',
            symbol1 + '_Close',
            
            symbol2 + '_Open',
            symbol2 + '_High',
            symbol2 + '_Low',
            symbol2 + '_Close',
            
            symbol2+'/'+symbol1]

        ticker_main_df = pd.concat(ticker_main, axis=1, keys=headers)
        
        return ticker_main_df
    
    def zScoreDF(ticker_main_df,rolling_window,symbol1,symbol2):
        ticker_main_df[symbol1 + '_log'] = np.log(ticker_main_df[symbol1 + '_Close'])
        ticker_main_df[symbol2 + '_log'] = np.log(ticker_main_df[symbol2 + '_Close'])

        regression_model = RollingOLS(ticker_main_df[symbol1 + '_log'], ticker_main_df[symbol2 + '_log'],rolling_window)
        rolling_res = regression_model.fit()

        ticker_main_df['Hedge_Ratio'] = rolling_res.params

        ticker_main_df['Distance'] = ticker_main_df[symbol1 + '_log'] 
        - (ticker_main_df['Hedge_Ratio'] * ticker_main_df[symbol2 + '_log'])

        ticker_main_df['Mean_Dist'] = ticker_main_df['Distance'].rolling(rolling_window).mean()
        ticker_main_df['Std_Dist'] = ticker_main_df['Distance'].rolling(rolling_window).std()

        ticker_main_df['Z_Score'] = (ticker_main_df['Distance'] - ticker_main_df['Mean_Dist'])/(ticker_main_df['Std_Dist'])
        
        return ticker_main_df
    
    def plotSymbols(ticker_main_df,symbol1,symbol2):
        fig, axes = plt.subplots(nrows=3, ncols=1)

        plt.subplot(3,1,1)
        plt.plot(ticker_main_df[symbol1 + '_Close'])
        plt.title(symbol1)

        plt.subplot(3,1,2)
        plt.plot(ticker_main_df[symbol2 + '_Close'])
        plt.title(symbol2)

        plt.subplot(3,1,3)
        plt.plot(ticker_main_df[symbol2+'/'+symbol1])
        plt.title(symbol2+'/'+symbol1)

        fig.tight_layout()
        plt.show()
    
    def plotZScore(ticker_main_df):
        fig = plt.figure()
        plt.plot(ticker_main_df['Z_Score'])
        plt.axhline(y=0,color='b')
        plt.axhline(y=z_score_buy_threshold,color='tomato',linestyle='--')
        plt.axhline(y=z_score_short_threshold,color='tomato',linestyle='--')
        plt.title("Z - Score")
        plt.show()

    def resetAccount(starting_capital):
        current_balance = starting_capital
        balance_list = []

        ## -------------------------------------------------------------------------------------------------------
        order_status = OrderStatus.NO_ORDER
        trade_count = 0

        price_symbol1 = 0
        price_symbol2 = 0

        squareOff_price_symbol1 = 0
        squareOff_price_symbol2 = 0

        square_off_index = 0

        order_id_price_symbol1 =0
        order_id_price_symbol2 =0

        order_details_cols = ['count',
        'order_type',
        'balance_prior',
        'balance_post',
        'order_id_price_symbol1',
        'price_symbol1',
        'balance_alloc_symbol',
        'quantity_symbol1',
        'squareOff_price_symbol1',
        'squareOff_bal_symbol1',
        'order_id_price_symbol2',
        'price_symbol2',
        'balance_alloc_symbol2',
        'quantity_symbol2',
        'squareOff_price_symbol2',
        'squareOff_bal_symbol2']
        order_details = pd.DataFrame(data=[],columns=order_details_cols)
        
        return (current_balance,balance_list,order_status,trade_count,
                price_symbol1,price_symbol2,squareOff_price_symbol1,squareOff_price_symbol2,
                square_off_index, order_id_price_symbol1,order_id_price_symbol2,
                order_details_cols,order_details
            )
    
    def runAnalysis(starting_capital,
                    algo_stop_balance,
                    sell_periods,
                    leverage,
                    transaction_fee,
                    z_score_buy_threshold,
                    z_score_short_threshold,
                    symbol1,symbol2,ticker_main_df
                    ):
        
        ## Reset Everything
        current_balance = starting_capital
        balance_list = []

        ## -------------------------------------------------------------------------------------------------------
        order_status = OrderStatus.NO_ORDER
        trade_count = 0

        price_symbol1 = 0
        price_symbol2 = 0

        squareOff_price_symbol1 = 0
        squareOff_price_symbol2 = 0

        square_off_index = 0

        order_id_price_symbol1 =0
        order_id_price_symbol2 =0

        order_details_cols = ['count',
        'order_type',
        'balance_prior',
        'balance_post',
        'order_id_price_symbol1',
        'price_symbol1',
        'balance_alloc_symbol',
        'quantity_symbol1',
        'squareOff_price_symbol1',
        'squareOff_bal_symbol1',
        'order_id_price_symbol2',
        'price_symbol2',
        'balance_alloc_symbol2',
        'quantity_symbol2',
        'squareOff_price_symbol2',
        'squareOff_bal_symbol2']
        order_details = pd.DataFrame(data=[],columns=order_details_cols)
        
        for index,row in ticker_main_df.iterrows():
            #print(index)
            ## Price of 1st Asset
            current_price_symbol1 = row[symbol1 + '_Close']
            
            ## Price of 2nd Asset
            current_price_symbol2 = row[symbol2 + '_Close']
            
            ## Z Score at the moment
            z_score = row["Z_Score"]
            
            ## For a Valid Portfolio Balance
            if current_balance > algo_stop_balance:
    #         if(order_status == OrderStatus.NO_ORDER and (z_score <= z_score_buy_threshold
    #                                                     or z_score >= z_score_short_threshold)):
                
    #             order_status = OrderStatus.NEXT_ORDER
                
    #             order_id_price_symbol1 = current_price_symbol1
    #             order_id_price_symbol2 = current_price_symbol2
                
                ## If there is no existing order in place, and Z-Score is below Buy Threshold!
                if(order_status == OrderStatus.NO_ORDER and z_score <= z_score_buy_threshold):
                    ## Long Order Initialized
                    #print('Long Order Initialized!')
                    order_status = OrderStatus.LONG
                    
                    ## Increment Trade Count 
                    trade_count = trade_count + 1
                    
                    ## Set Square off Condition
                    square_off_index = index + sell_periods
                    
                    ## Long Symbol 1 and Short Symbol 2
                    price_symbol1 = current_price_symbol1
                    price_symbol2 = current_price_symbol2
                    
                    
                if(order_status == OrderStatus.NO_ORDER and z_score >= z_score_short_threshold):
                    ## Short Order Initialized
                    #print('Short Order Initialized!')
                    order_status = OrderStatus.SHORT
                    
                    ## Increment Trade Count 
                    trade_count = trade_count + 1
                    
                    ## Set Square off Condition
                    square_off_index = index + sell_periods
                    
                    ## Short Symbol 1 and Long Symbol 2
                    price_symbol1 = current_price_symbol1
                    price_symbol2 = current_price_symbol2
                
                
                if(order_status != OrderStatus.NO_ORDER):
                    
                    ## Square off
                    if(index == square_off_index):
                        
                        ## Update Square off prices
                        squareOff_price_symbol1 = current_price_symbol1
                        squareOff_price_symbol2 = current_price_symbol2
                        
                        ## Balance Allocation for Positions (inclusive of leverage)
                        balance_alloc_symbol1 = 0.5  * leverage * current_balance
                        balance_alloc_symbol2 = 0.5  * leverage * current_balance
                        
                        
                        ##Long Square Off
                        if(order_status == OrderStatus.LONG):
                            ## Buy Quantity (inclusive of Transaction Fee Deductions)
                            quantity_symbol1 = ((1 - transaction_fee) 
                                                * (balance_alloc_symbol1/price_symbol1))
                            ## Since Symbol2 is Shorted its Buy quantity is calcualted based on the squareoff price
                            quantity_symbol2 = ((1 - transaction_fee) 
                                                * (balance_alloc_symbol2/squareOff_price_symbol2))
                            
                            ## Balance after Square Off i.e Selling the bought quantity
                            squareOff_bal_symbol1 = ((1 - transaction_fee) 
                                                    * (squareOff_price_symbol1 * quantity_symbol1))/leverage

                            squareOff_bal_symbol2 = ((1 - transaction_fee) 
                                                    * (price_symbol2 * quantity_symbol2))/leverage
                            
                        ##Short Square Off
                        if(order_status == OrderStatus.SHORT):
                            ## Buy Quantity (inclusive of Transaction Fee Deductions)
                            ## Since Symbol2 is Shorted its Buy quantity is calcualted based on the squareoff price
                            quantity_symbol1= ((1 - transaction_fee) 
                                                * (balance_alloc_symbol1/squareOff_price_symbol1))
                            
                            quantity_symbol2 = ((1 - transaction_fee) 
                                                * (balance_alloc_symbol2/price_symbol2))
                            
                            
                            ## Balance after Square Off i.e Selling the bought quantity
                            squareOff_bal_symbol1 = ((1 - transaction_fee) 
                                                    * (price_symbol1 * quantity_symbol1))/leverage
                            
                            squareOff_bal_symbol2 = ((1 - transaction_fee) 
                                                    * (squareOff_price_symbol2 * quantity_symbol2))/leverage
                        
                        #print('Order Squares Off!')
                        resultant_balance = squareOff_bal_symbol1 + squareOff_bal_symbol2
                        
                        order_details = order_details.append(pd.DataFrame(data=[[
                            trade_count,
                            order_status,
                            current_balance,
                            resultant_balance,
                            order_id_price_symbol1,
                            price_symbol1,
                            balance_alloc_symbol1,
                            quantity_symbol1,
                            squareOff_price_symbol1,
                            squareOff_bal_symbol1,
                            order_id_price_symbol2,
                            price_symbol2,
                            balance_alloc_symbol2,
                            quantity_symbol2,
                            squareOff_price_symbol2,
                            squareOff_bal_symbol2,
                        ]],columns=order_details_cols))
                        
                        current_balance = resultant_balance
                        order_status = OrderStatus.NO_ORDER
                        
                balance_list.append(current_balance)
        
        return current_balance,balance_list,order_details

## -------------------------------------------------------------


### Load Data from CSV
# past_dataframe_symbol1,past_dataframe_symbol2 = loadSymbolsFromCSV()

# ### Construct Main Data Frame

# ticker_main = [
#     past_dataframe_symbol1.close,
#     past_dataframe_symbol2.close,
#     past_dataframe_symbol2.close/past_dataframe_symbol1.close]

# headers = [symbol1,symbol2,symbolcomposite]
# ticker_main_df = pd.concat(ticker_main, axis=1, keys=headers)
# ticker_main_df
