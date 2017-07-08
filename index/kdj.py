# -*- coding: utf-8 -*-
from index.rsv import RSV
from functools import reduce


class KDJ:
    def __init__(self, period=9, m1=3, m2=3):
        self.perid = period
        self.m1 = m1
        self.m2 = m2
        self._rsv_calc = RSV(period)
        self.cache = {"id": None, "k": None, "d": None, "j": None}
        self._k = 50
        self._d = 50

    def __call__(self, item):
        identifier, value = item
        rsv = self._rsv_calc(item)
        if not rsv is None:
            self.cache["id"] = [self.cache["id"], identifier][self.cache["id"] is None]
            if identifier != self.cache["id"]:
                self._k = self.cache["k"]
                self._d = self.cache["d"]
                self.cache["id"] = identifier
            self.cache["k"] = (2 / self.m2) * self._k + (1 / self.m1) * rsv
            self.cache["d"] = (2 / self.m2) * self._d + (1 / self.m1) * self.cache["k"]
            self.cache["j"] = 3 * self.cache["d"] - 2 * self.cache["k"]
        return {"id": identifier,
                "rsv": rsv,
                "k": self.cache["k"],
                "d": self.cache["d"],
                "j":self.cache["j"]}
