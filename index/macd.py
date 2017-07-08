# -*- coding :utf-8 -*-
from index.ema import EMA


class MACD:
    def __init__(self, short=12, long=26, mid=9):
        self._dif_calc = {"short": EMA(short), "long": EMA(long)}
        self._dea_calc = EMA(mid)
        self.dif = None
        self.dea = None
        self.macd = None

    def __call__(self, item):
        identifier, value = item
        self.dif = self._dif_calc["short"](item) - self._dif_calc["long"](item)
        self.dea = self._dea_calc((identifier, self.dif))
        self.macd = 2 * (self.dif - self.dea)
        return {"id": identifier, "dif": self.dif, "dea": self.dea, "macd": self.macd}
