# Config Import -------------------------------------------------------------------------------------
from configs.config import *
# Library Imports -----------------------------------------------------------------------------------
import backtrader as bt
from backtrader_plotting import Bokeh, OptBrowser
from backtrader_plotting.schemes import Blackly, Tradimo
import pyfolio as pf
import pandas as pd
# Local Imports -------------------------------------------------------------------------------------
from core.strategies.sma.sma_crossover import SmaCross
from core.analyzers.analyzerprinter import AnalyzerPrinter


# Class Begin ---------------------------------------------------------------------------------------
class CommInfoFractional(bt.CommissionInfo):
    params = (
        ('commission', commission), ('mult', multiplier), ('margin', True),
        ('commtype', bt.CommInfoBase.COMM_PERC),
        ('stocklike', False),
        ('leverage', multiplier),
        ('automargin', 1),
    )

    def getsize(self, price, cash):

        return self.p.leverage * (cash / price)


class Backtest:
    """
    A class for running the backtest
    """

    def __init__(self):
        self.cerebro = bt.Cerebro()

        self.add_sizer()
        self.setup_broker()
        self.add_data()
        self.add_stategy()
        self.add_analysers()

        thestrat = self.run_strategy()
        self.print_analysis(thestrat)
        b = Bokeh(style='bar', plot_mode='single', scheme=Blackly())
        self.cerebro.plot(b, iplot=False)

    def add_sizer(self):
        self.cerebro.addsizer(bt.sizers.PercentSizer, percents=90, retint=False)

    def setup_broker(self):
        """
        Setup the broker
        :return:
        """
        self.cerebro.broker.setcash(inital_cash)

        self.cerebro.broker.setcommission(commission=commission,
                                          margin=True,
                                          # mult=multiplier,
                                          leverage=multiplier,
                                          commtype=bt.CommInfoBase.COMM_PERC,
                                          stocklike=False,
                                          automargin=1
                                          )
        # self.cerebro.broker.addcommissioninfo(CommInfoFractional())
        print('Starting Portfolio Value: %.2f' % self.cerebro.broker.getvalue())

    def add_data(self):
        """
        Loads the data from a csv file for the backtest
        :return:
        """

        # Add lower timeframe ticker
        dataframe_lowerframe = pd.read_csv(csv_path_lowerframe, parse_dates=True, index_col=0)
        data_lowerframe = bt.feeds.PandasData(dataname=dataframe_lowerframe)
        self.cerebro.adddata(data_lowerframe)

        # Add higher timeframe ticker
        dataframe_higherframe = pd.read_csv(csv_path_higherframe, parse_dates=True, index_col=0)
        data_higherframe = bt.feeds.PandasData(dataname=dataframe_higherframe)
        self.cerebro.adddata(data_higherframe)

    def add_stategy(self):
        self.cerebro.addstrategy(SmaCross)

    def add_analysers(self):
        """
        Adds various analysers for the backtest
        :return:
        """
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
        self.cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        # self.cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')

    def run_strategy(self):
        thestrats = self.cerebro.run()
        thestrat = thestrats[0]
        return thestrat

    @staticmethod
    def print_analysis(thestrat):
        """
        Print the results of the analysers
        :param thestrat:
        :return:
        """
        AnalyzerPrinter.print_trade_analysis(thestrat.analyzers.ta.get_analysis())
        AnalyzerPrinter.print_sqn_analysis(thestrat.analyzers.sqn.get_analysis())
        AnalyzerPrinter.print_sharpe_analysis(thestrat.analyzers.sharpe.get_analysis())

    @staticmethod
    def pyfolio_analysis(thestrat):
        """
        Pyfolio Analyszer, works the best with Jupyter Notebook
        :param thestrat:
        :return:
        """
        pyfolio_analysis = thestrat.analyzers.pyfolio.get_analysis()

        returns = pyfolio_analysis['returns']
        positions = pyfolio_analysis['positions']
        transactions = pyfolio_analysis['transactions']
        gross_lev = pyfolio_analysis['gross_lev']

        returns_series = pd.DataFrame({'date': pd.Series(returns.keys()), 'returns': pd.Series(returns.values())})\
            .set_index('date').returns

        # pf.create_returns_tear_sheet(returns_series)
# Class End -----------------------------------------------------------------------------------------
