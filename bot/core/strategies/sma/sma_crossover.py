from datetime import datetime
import backtrader as bt

# Create a subclass of Strategy to define the indicators and logic


class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=50,  # period for the fast moving average
        pslow=200,   # period for the slow moving average
        multi=True
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.buyprice = None
        self.buycomm = None
        self.opsize = None
        # noinspection PyUnresolvedReferences
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        # noinspection PyUnresolvedReferences
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                # self.buy()
                self.order_target_percent(target=1)
        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()
        # else:
        #     self.log('Price: %.2f, Value in Trade : %.2f $' %
        #              (self.data.tick_high, self.broker.getvalue()))

    def notify(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.status == order.Canceled:
                self.log("Order Cancelled")
            elif order.status == order.Completed or order.status == order.Margin:
                if order.isbuy():
                    self.log(
                        'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                        (order.executed.price,
                         order.executed.value,
                         order.executed.comm))

                    self.buyprice = order.executed.price
                    self.buycomm = order.executed.comm
                    self.opsize = order.executed.size

                elif order.issell():  # Sell

                    self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f, PNL: %.2f' %
                             (order.executed.price,
                              order.executed.value,
                              order.executed.comm,
                              order.executed.pnl
                              ))
                    self.log('Cash After Trade : %.2f $' %
                             (self.broker.getcash()))
                    self.log('Value After Trade : %.2f $' %
                             (self.broker.getvalue()))
