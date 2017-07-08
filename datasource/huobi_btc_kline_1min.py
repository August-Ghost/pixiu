# -*- coding: utf-8 -*-
from datasource.huobi_kline import HuobiKline
from api.huobi_api import HuobiAPI_LTC_BTC


class HuobiBtcKline1min(HuobiKline):
    def config(self):
        self.configure = {
            "name": "huobi_btc_kline_1min",  # Required. Your strategy need this to get data.

            "query_config":{
                "api": HuobiAPI_LTC_BTC().stock(market="CNY").btc_kline_001_json,
            },
        }


EXPORT = HuobiBtcKline1min
