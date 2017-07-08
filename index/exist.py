# -*- coding: utf-8 -*-
from collections import deque
from functools import reduce


class Exist:
    def __init__(self, period):
        self.queue = deque(iterable=(False for i in range(0, period)),
                           maxlen=period)
        self.chunk_id = None

    def __call__(self, item):
        identifier, value = item
        if identifier != self.chunk_id:
            self.queue.append(not not value)
            self.chunk_id = identifier
        else:
            self.queue[-1] = not not value
        result =  reduce(lambda accumulated, updated: accumulated or updated,
                      self.queue, False)
        return result