# -*- coding: utf-8 -*-
from mainframe.ecdatasource import ECDataSource
from datetime import datetime
import json


class HuobiKline(ECDataSource):

    async def __call__(self, **params):
        p = {**params}
        if "length" not in params:
            p["length"] = 1
        p["length"] = min(p["length"], 2000)
        raw = self.configure["query_config"]["api"](**p)
        query_param = {**raw,
                       "url": raw["url"] + "?" + raw["params"],}
        del query_param["params"]
        return await self.query(**query_param)

    def parse_json(self, json_response):
        return tuple({"timestamp": int(datetime.strptime(j[0][:-5],
                                                         "%Y%m%d%H%M").timestamp()),
                      "open": j[1],
                      "high": j[2],
                      "low": j[3],
                      "close": j[4],
                      "vol": j[5], } for j in json_response)

    async def process_response(self, response):
        return self.parse_json(json.loads(response))
