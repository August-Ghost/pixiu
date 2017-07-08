# -*- coding: utf-8 -*-
from mainframe.ecdatasource import ECDataSource
from api.huobi_api import HuobiAPI_LTC_BTC
import json


class HuobiLtcDetail(ECDataSource):
    def config(self):
        self.configure = {
            "name": "huobi_ltc_detail",  # Required. Your strategy need this to get data.

            "query_config":{
                "api": HuobiAPI_LTC_BTC().stock(market="CNY").detail_ltc_json,
            },
        }

    async def __call__(self):
        raw = self.configure["query_config"]["api"]()
        return await self.query(**{"url": raw["url"] + "?" + raw["params"], "method": "GET"})

    async def process_response(self, response):
        return json.loads(response)


EXPORT = HuobiLtcDetail
