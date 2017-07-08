# -*- coding: utf-8 -*-
from datasource.huobi_kline import HuobiKline
from api.huobi_api import HuobiAPI_LTC_BTC


class HuobiBtcKline1year(HuobiKline):
    def config(self):
        self.configure = {
            "name": "huobi_btc_kline_1year",  # Required. Your strategy need this to get data.

            "query_config":{
                "api": HuobiAPI_LTC_BTC().stock(market="CNY").btc_kline_400_json,
            },
        }


EXPORT = HuobiBtcKline1year
