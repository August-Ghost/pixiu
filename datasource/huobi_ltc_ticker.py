# -*- coding: utf-8 -*-
from mainframe.ecdatasource import ECDataSource
from api.huobi_api import HuobiAPI_LTC_BTC
import json


class HuobiLtcTicker(ECDataSource):
    def config(self):
        self.configure = {
            "name": "huobi_ltc_ticker",  # Required. Your strategy need this to get data.

            "query_config":{
                "api": HuobiAPI_LTC_BTC().stock(market="CNY").ticker_ltc_json,
            },
        }

    async def __call__(self):
        raw = self.configure["query_config"]["api"]()
        return await self.query(**{"url": raw["url"] + "?" + raw["params"], "method": "GET"})

    def parse_json(self, json_response):
        return {"timestamp": int(json_response["time"]),
                 "high": json_response["ticker"]["high"],
                 "low": json_response["ticker"]["low"],
                 "close": json_response["ticker"]["last"],
                 "vol": json_response["ticker"]["vol"],
                 "buy": json_response["ticker"]["buy"],
                 "sell": json_response["ticker"]["sell"]}

    async def process_response(self, response):
        return self.parse_json(json.loads(response))


EXPORT = HuobiLtcTicker
