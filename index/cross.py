# -*- coding:utf-8 -*-
from collections import deque



class Cross:
    def __init__(self):
        self.line1_cache = deque(maxlen=2)
        self.line2_cache = deque(maxlen=2)
        self.register = {"line1_id": None,
                         "line2_id": None}

    def __call__(self, line1_item, line2_item):
        id1, value1 = line1_item
        id2, value2 = line2_item
        if not value1 is None and not value2 is None:
            if id1 != self.register["line1_id"]:
                self.register["line1_id"] = id1
                self.line1_cache.append(value1)
            else:
                self.line1_cache[-1] = value1

            if id2 != self.register["line2_id"]:
                self.register["line2_id"] = id2
                self.line2_cache.append(value2)
            else:
                self.line2_cache[-1] = value2
            return (self.line1_cache[0] < self.line2_cache[0]
                    and self.line1_cache[-1] >= self.line2_cache[-1])


