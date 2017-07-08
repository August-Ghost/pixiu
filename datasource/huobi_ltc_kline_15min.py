# -*- coding: utf-8 -*-
from datasource.huobi_kline import HuobiKline
from api.huobi_api import HuobiAPI_LTC_BTC


class HuobiLtcKline15min(HuobiKline):
    def config(self):
        self.configure = {
            "name": "huobi_ltc_kline_15min",  # Required. Your strategy need this to get data.

            "query_config":{
                "api": HuobiAPI_LTC_BTC().stock(market="CNY").ltc_kline_015_json,
            },
        }


EXPORT = HuobiLtcKline15min
