# Config Import -------------------------------------------------------------------------------------
from configs.config import *
# Library Imports -----------------------------------------------------------------------------------
import backtrader as bt
# Local Imports -------------------------------------------------------------------------------------
from core.strategies.sma.sma_crossover import SmaCross
from core.analyzers.analyzerprinter import AnalyzerPrinter
import pyfolio as pf
import pandas as pd


# Class Begin ---------------------------------------------------------------------------------------


class Backtest:
    """
    A class for running the backtest
    """

    def __init__(self):
        self.cerebro = bt.Cerebro()

        self.cerebro.broker.setcash(inital_cash)
        self.cerebro.broker.setcommission(commission=commission, mult=multiplier,
                                          commtype=bt.CommInfoBase.COMM_PERC,
                                          automargin=auto_margin)
        print('Starting Portfolio Value: %.2f' % self.cerebro.broker.getvalue())

        self.load_data()

        self.cerebro.addstrategy(SmaCross)
        self.add_analysers()
        thestrats = self.cerebro.run()
        thestrat = thestrats[0]

        pyfolio_analysis = thestrat.analyzers.pyfolio.get_analysis()
        AnalyzerPrinter.print_trade_analysis(thestrat.analyzers.ta.get_analysis())
        AnalyzerPrinter.print_sqn_analysis(thestrat.analyzers.sqn.get_analysis())
        AnalyzerPrinter.print_sharpe_analysis(thestrat.analyzers.sharpe.get_analysis())

        print('Final Portfolio Value: %.2f' % self.cerebro.broker.getvalue())
        returns, positions, transactions, gross_lev = \
            pyfolio_analysis['returns'], pyfolio_analysis['positions'], \
            pyfolio_analysis['transactions'], pyfolio_analysis['gross_lev']
        # returns = pd.DataFrame(returns, columns=returns.keys())
        pf.create_returns_tear_sheet(pd.DataFrame({'date': pd.Series(returns.keys()),
                                                   'returns': pd.Series(returns.values())}).set_index('date').returns)
        # self.cerebro.plot(style='bar')

    def load_data(self):
        """
        Loads the data from a csv file for the backtest
        :return:
        """
        dataframe = pd.read_csv(csv_path_higherframe, parse_dates=True, index_col=0)
        data = bt.feeds.PandasData(dataname=dataframe)

        self.cerebro.adddata(data)

    def add_analysers(self):
        """
        Adds various analysers for the backtest
        :return:
        """
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
        self.cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        self.cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')


# Class End -----------------------------------------------------------------------------------------
