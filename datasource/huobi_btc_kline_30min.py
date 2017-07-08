# -*- coding: utf-8 -*-
from datasource.huobi_kline import HuobiKline
from api.huobi_api import HuobiAPI_LTC_BTC


class HuobiBtcKline30min(HuobiKline):
    def config(self):
        self.configure = {
            "name": "huobi_btc_kline_30min",  # Required. Your strategy need this to get data.

            "query_config":{
                "api": HuobiAPI_LTC_BTC().stock(market="CNY").btc_kline_030_json,
            },
        }


EXPORT = HuobiBtcKline30min
