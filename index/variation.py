# -*- coding: utf-8 -*-
from collections import deque
from operator import sub


class Variation:
    def __init__(self):
        self.chunk_id = None
        self.reg = deque(iterable=(0, 0), maxlen=2)

    def __call__(self, item):
        identifier, value = item
        if identifier != self.chunk_id:
            self.reg.append(value)
            self.chunk_id = identifier
        else:
            self.reg[-1] = value
        return -sub(*self.reg)