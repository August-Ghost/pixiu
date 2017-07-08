# -*- coding: utf-8 -*-


class EMA:
    def __init__(self, period):
        self.previous = None
        self.cache = {"id": None, "result": None}
        self.ema_param = (2 / (period + 1))

    def __call__(self, item):
        identifier, value = item
        # Init cache
        self.cache["id"] = [self.cache["id"], identifier][self.cache["id"] is None]
        if identifier != self.cache["id"]:
            self.previous = self.cache["result"]
            self.cache["id"] = identifier
        result = value if self.previous is None \
            else (value - self.previous) * self.ema_param + self.previous
        # For each id-value pair, we will keep the result in self.previous only
        # if the calculated result is stable.
        self.cache["result"] = result
        return result
