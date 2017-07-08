# -*- coding:utf-8 -*-
from mainframe.ecstrategy import ECTradeStrategy
from index.ma import MA


class TradeStrategy_traceback_test(ECTradeStrategy):
    async def init(self):
        # Init strategy, like setting up index you need.
        # By default, your strategy will be called every seconds.
        # If set period to 0, the strategy will only be called once.
        self.period = 0 # msecond.

    async def process(self):
        # Write your strategy here.
        # Good hunting :)
        data = await self.huobi_ltc_kline_1min(length=2000)
        for i in data:
            # Separate timestamp
            print(i["timestamp"], self.ma((i["timestamp"], i["close"])))


EXPORT = TradeStrategy_traceback_test
