# -*- coding:utf-8 -*-
from mainframe.ecstrategy import ECTradeStrategy
from index.ma import MA
from trader.huobi_dummytrader import Huobi_SimpleDummyTrader


class TradeStrategy_index_test(ECTradeStrategy):
    def init(self):
        # Init strategy, like setting up index you need.
        # By default, your strategy will be called every seconds.
        # If set period to 0, the strategy will only be called once.
        self.period = 1000 # msecond.
        self.ma = MA(5)
        self.trader = Huobi_SimpleDummyTrader(currency=10000)

    async def cold_start(self):
        # Use historical data to activate the index
        init_data = await self.huobi_ltc_kline_1min(length=2000)
        for i in init_data[:-1]:
            # Separate timestamp
            self.ma((i["timestamp"], i["close"]))

    async def process(self):
        # Write your strategy here.
        # Good hunting :)
        data = await self.huobi_ltc_ticker()
        # Separate timestamp
        print(self.ma((data["timestamp"], data["close"])))


EXPORT = TradeStrategy_index_test
