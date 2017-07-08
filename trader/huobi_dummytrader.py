# -*- coding: utf-8 -*-
from datasource.huobi_ltc_detail import HuobiLtcDetail
from datasource.huobi_btc_detail import HuobiBtcDetail


class Huobi_SimpleDummyTrader:
    def __init__(self, currency=100000, ltc=0, btc=0):
        self.currency = currency
        self.ltc = ltc
        self.btc = btc
        self.btc_detail = HuobiBtcDetail()
        self.ltc_detail = HuobiLtcDetail()

    async def buy(self, coin_type, price=None):
        """
        Purchase coin at market price (only support huobi.com.),
         If price is given, purchase at the price.
        :param coin_type: The type of the coin to buy. 1: BTC, 2: LTC.
        :param price: Purchase at this price.
        :return: account info
        """
        return (await self._simulation_buy(coin_type)) if not price else (await self._traceback_buy(coin_type, price))

    async def _simulation_buy(self, coin_type):
        """
        Purchase coin at market price (only support huobi.com.)
        """
        if coin_type == 1:
            buy_1 = (await self.btc_detail())["top_buy"][0]
            if self.currency:
                self.btc += (self.currency / buy_1["price"]) * 0.998
                self.currency = 0
                return {"currency": self.currency,
                        "ltc": self.ltc,
                        "btc": self.btc}
        elif coin_type == 2:
            buy_1 = (await self.ltc_detail())["top_buy"][0]
            if self.currency:
                self.ltc += (self.currency / buy_1["price"]) * 0.998
                self.currency = 0
                return {"currency": self.currency,
                        "ltc": self.ltc,
                        "btc": self.btc}
        else:
            raise AttributeError("coin_type must be 1 for BTC or 2 for LTC.")

    async def _traceback_buy(self, coin_type, price):
        """
        Purchase at given price. Useful for traceback.
        """
        if self.currency:
            if coin_type == 1:
                self.btc += (self.currency / price) * 0.998
            elif coin_type == 2:
                self.ltc += (self.currency / price) * 0.998
            else:
                raise AttributeError("coin_type must be 1 for BTC or 2 for LTC.")
            self.currency = 0
            return {"currency": self.currency,
                    "ltc": self.ltc,
                    "btc": self.btc}

    async def sell(self, coin_type, price=None):
        """
        Sell coin at market price (only support huobi.com.),
         If price is given, purchase at the price.
        :param coin_type: The type of the coin to buy. 1: BTC, 2: LTC.
        :return: account info
        """
        return (await self._simulation_sell(coin_type)) if not price else (await self._traceback_sell(coin_type, price))

    async def _simulation_sell(self, coin_type):
        """
        Sell coin at market price (only support huobi.com.)
        """
        if coin_type == 1:
            if self.btc:
                sell_1 = (await self.btc_detail())["top_sell"][0]
                self.currency += (self.btc * sell_1["price"]) * 0.998
                self.btc = 0
                return {"currency": self.currency,
                        "ltc": self.ltc,
                        "btc": self.btc}
        elif coin_type == 2:
            if self.ltc:
                sell_1 = (await self.ltc_detail())["top_sell"][0]
                self.currency += (self.ltc * sell_1["price"]) * 0.998
                self.ltc = 0
                return {"currency": self.currency,
                        "ltc": self.ltc,
                        "btc": self.btc}
        else:
            raise AttributeError("coin_type must be 1 for BTC or 2 for LTC.")

    async def _traceback_sell(self, coin_type, price):
        """
        Sell coin at given price. Useful for traceback.
        """
        if coin_type == 1:
            if self.btc:
              self.currency += (self.btc * price) * 0.998
              self.btc = 0
              return {"currency": self.currency,
                      "ltc": self.ltc,
                      "btc": self.btc}
        elif coin_type == 2:
            if self.ltc:
                self.currency += (self.ltc * price) * 0.998
                self.ltc = 0
                return {"currency": self.currency,
                        "ltc": self.ltc,
                        "btc": self.btc}
        else:
            raise AttributeError("coin_type must be 1 for BTC or 2 for LTC.")

    def __repr__(self):
        return str({"currency": self.currency,
                    "ltc": self.ltc,
                    "btc": self.btc})



if __name__ == '__main__':
    dt = Huobi_SimpleDummyTrader()
    print(dt.buy(1, 17999))

