# -*- coding: utf-8 -*-
from mainframe.ecdatasource import ECDataSource
from api.huobi_api import HuobiAPI_LTC_BTC
from pandas import DataFrame
from datetime import datetime
import json


class Huobi_Ltc_kline_3min(ECDataSource):
    def config(self):
        self.configure = {
            "name": "huobi_ltc_kline_3min",  # Required. Your strategy need this to get data.

            "query_config": {
                "api": HuobiAPI_LTC_BTC().stock(market="CNY").ltc_kline_001_json,
            },
        }

    async def __call__(self, **params):
        p = {**params}
        if "length" not in params:
            p["length"] = 1
        p["length"] = min(p["length"] * 3, 2000)

        raw = self.configure["query_config"]["api"](**p)
        query_param = {**raw,
                       "url": raw["url"] + "?" + raw["params"], }
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
        parsed = self.parse_json(json.loads(response))
        data_df = DataFrame.from_records(parsed)
        # Is there any better solution?
        result = tuple({"timestamp": df["timestamp"].max(),
                        "open": df[df["timestamp"] == df["timestamp"].min()]["open"].iloc[0],
                        "high": df["high"].max(),
                        "low": df["low"].min(),
                        "close": df[df["timestamp"] == df["timestamp"].max()]["close"].iloc[0],
                        "vol": df["vol"].sum()} for df in (data_df.iloc[chunk_id * 3: chunk_id * 3 + 3] for chunk_id in range(0, len(parsed) // 3)))
        return result

