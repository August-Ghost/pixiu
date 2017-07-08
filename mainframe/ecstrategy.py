# -*- coding:utf-8 -*-
from base.basestrategy import BaseStrategy


class ECTradeStrategy(BaseStrategy):
    def __init__(self, datatsource):
        self.trader = None
        super(ECTradeStrategy, self).__init__(datatsource)