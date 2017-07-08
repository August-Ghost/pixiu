# -*- coding: utf-8 -*-
from collections import deque


class RSV:
    def __init__(self, period):
        self.chunk_id = None
        self.period = period
        self.queue = deque(maxlen=period)

    def __call__(self, item):
        """
        Calculating RSV dynamically.
        :param item: Tuple of  2 elements. The first element is identifier.
        :return: rsv value based on given input.
        """
        identifier, value = item
        if identifier != self.chunk_id:
            self.queue.append(value)
            self.chunk_id = identifier
        else:
            self.queue[-1] = value
        if len(self.queue) == self.period:
            result = (self.queue[-1]["close"] - min(i["low"] for i in self.queue)) /\
                             (max(i["high"] for i in self.queue) - min(i["low"] for i in self.queue)) * 100
            return result
