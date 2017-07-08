# -*- coding: utf-8 -*-
from collections import deque


class Delay:
    def __init__(self, period):
        self.chunk_id = None
        self.queue = deque(iterable=(None for i in range(0, period)), maxlen=period)

    def __call__(self, item):
        identifier, value = item
        if identifier != self.chunk_id:
            self.queue.append(value)
            self.chunk_id = identifier
        else:
            self.queue[-1] = value
        return self.queue[0]