# -*- coding: utf-8 -*-
from collections import deque
from index.ma import MA
from math import sqrt
from functools import reduce
from operator import add




class Boll:
    def __init__(self, period=20):
        self.period = period
        self.ma = MA(period)
        self.queue = deque(maxlen=period)
        self.chunk_id = None

    def __call__(self, item):
        identifier, value = item

        ma  = self.ma((identifier, value["close"]))
        if ma:
            if identifier != self.chunk_id:
                self.chunk_id = identifier
                self.queue.append((value["close"] - ma) ** 2)
            else:
                self.queue[-1] = (value["close"] - ma) ** 2
            stdev = sqrt(reduce(add, self.queue) / self.period)
            return {"upper": ma + 2 * stdev,
                    "lower": ma - 2 * stdev,
                    "mid": ma, **value}


