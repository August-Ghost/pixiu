# -*- coding: utf-8 -*-
from mainframe.ecdatasource import ECDataSource
from api.huobi_api import HuobiAPI_LTC_BTC
from datetime import datetime
import json



class HuobiLtcKline30min(ECDataSource):
    def config(self):
        self.configure = {
            "name": "huobi_ltc_kline_30min",  # Required. Your strategy need this to get data.

            "query_config":{
                "api": HuobiAPI_LTC_BTC().stock(market="CNY").ltc_kline_030_json,
            },
        }


EXPORT = HuobiLtcKline30min
