# -*- coding: utf-8 -*-
from collections import deque
from functools import reduce
from operator import add


class MA:
    def __init__(self, period):
        self.chunk_id = None
        self.period = period
        self.queue = deque(maxlen=period)

    def __call__(self, item):
        """
        Calculating Moving average dynamically.
        :param item: Tuple of  2 elements. The first element is identifier.
        :return: Moving average value based on given input.
        """
        identifier, value = item
        if identifier != self.chunk_id:
            self.queue.append(value)
            self.chunk_id = identifier
        else:
            self.queue[-1] = value
        if len(self.queue) == self.period:
            return reduce(add, self.queue) / self.period
        else:
            return None
