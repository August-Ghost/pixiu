# -*- coding: utf-8 -*-
from urllib.parse import urlunsplit, SplitResult, urljoin, urlencode
from hashlib import md5
from os.path import basename
from time import time



class HuobiBaseAPI:
    Stock_API_netloc = None
    Trade_API_netloc = None

    def __init__(self, secret_key=None, **kargs):
        self.secret_key = secret_key
        self.request_buffer = {"scheme": "https",
                               "netloc": "",
                               "path": "",
                               "query": "",
                               "fragment": ""
                               }
        self.request_buffer.update(kargs)

    def update_request_path(self, path):
        self.request_buffer["path"] = urljoin(self.request_buffer["path"] + "/", path)

    def __call__(self, **kwargs):
        if self.request_buffer:
            if self.request_buffer["netloc"] == type(self).Trade_API_netloc:
                return self.construct_trade_request(**kwargs)
            elif self.request_buffer["netloc"] == type(self).Stock_API_netloc:
                return self.construct_stock_request(**kwargs)

    def construct_trade_request(self, **kwargs):
        raise NotImplementedError

    def construct_stock_request(self, **kwargs):
        raise NotImplementedError

    def sign(self):
        raise NotImplementedError

    def trade(self):
        raise NotImplementedError

    def stock(self, market="CNY"):
        raise NotImplementedError

    def __getattr__(self, item):
        """
        For each node in path, we create a new instance
        """
        instance = type(self)(secret_key=self.secret_key,
                              **self.request_buffer)
        instance.update_request_path(item)
        return instance


class HuobiAPI_LTC_BTC(HuobiBaseAPI):
    Stock_API_netloc = r"api.huobi.com"
    Trade_API_netloc = r"api.huobi.com/apiv3"


    def sign(self, **kargs):
        params_to_sign = kargs
        params_to_sign.update({"secret_key": self.secret_key})
        urlencoded_params = urlencode(sorted(params_to_sign.items(), key=lambda item: item[0])).encode(encoding='utf-8')
        sign = md5(urlencoded_params).hexdigest()
        return sign

    def construct_stock_request(self, **kwargs):
        if not self.request_buffer["path"].endswith(".js"):
            self.request_buffer["path"] += ".js"
        return {"url": urlunsplit(SplitResult(**self.request_buffer)),
                "method": "GET",
                "params": urlencode(kwargs)}

    def construct_trade_request(self, **kwargs):
        query_args = {**kwargs,
                      "method": basename(self.request_buffer["path"])}
        extra = query_args.pop("extra", {})

        query_args.setdefault("created", int(time()))
        query_args["sign"] = self.sign(**query_args)
        query_args.update(extra)

        return {"url": urlunsplit(SplitResult(**self.request_buffer)),
                "method": "POST",
                "params": urlencode(query_args)}

    def trade(self):
        self.request_buffer["netloc"] = type(self).Trade_API_netloc
        instance = type(self)(secret_key=self.secret_key,
                              **self.request_buffer)
        return instance

    def stock(self, market="CNY"):
        mkt = {"CNY": "staticmarket", "USD": "usdmarket"}
        self.request_buffer["netloc"] = type(self).Stock_API_netloc
        self.request_buffer["path"] = urljoin(self.request_buffer["path"], mkt[market] + "/")
        instance = type(self)(secret_key=self.secret_key,
                              **self.request_buffer)
        return instance




if __name__ == "__main__":
    import requests
    payload = HuobiAPI_LTC_BTC().stock().ltc_kline_001_json(length=3)
    print(payload)
    del payload["method"]
    print(requests.get(**payload).content)
