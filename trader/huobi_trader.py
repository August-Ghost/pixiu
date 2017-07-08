# -*- coding: utf-8 -*-
from mainframe.ectrader import ECTrader
from api.huobi_api import HuobiAPI_LTC_BTC
import json


class Huobi_Trader(ECTrader):

    async def buy(self, amount, coin_type, price, **kargs):
        """

        :param amount: Total purchase amount.
        :param coin_type: The type of the coin to buy. 1: BTC, 2: LTC.
        :param price: Buy at this price.
        :param kargs:Additional params for buy.
        Please refer to: https://github.com/huobiapi/API_Docs/wiki/REST-buy
        :return:
        """
        additional_args = {"trade_password", "trade_id", "market"}
        q = {"amount": amount,
             "access_key": self.configure["access_key"],
             "price": price,
             "coin_type": coin_type,
             "extra": self._get_extra(additional_args, kargs)}
        return await self._query("buy", q)

    async def buy_market(self, amount, coin_type,**kargs):
        """

        :param amount: Total purchase amount.
        :param coin_type: The type of the coin to buy. 1: BTC, 2: LTC.
        :param kargs: Additional params for buy_market.
        Please refer to: https://github.com/huobiapi/API_Docs/wiki/REST-buy_market
        :return:
        """
        additional_args = {"trade_password", "trade_id", "market"}
        q = {"amount": amount,
             "access_key": self.configure["access_key"],
             "coin_type": coin_type,
             "extra": self._get_extra(additional_args, kargs)}
        return await self._query("buy_market", q)

    async def cancel_order(self, coin_type, order_id, **kargs):
        """
        :param coin_type: The type of the coin to buy. 1: BTC, 2: LTC.
        param order_id: order id to request.
        :param kargs: Additional params for order_info.
        Please refer to: https://github.com/huobiapi/API_Docs/wiki/REST-order_info
        :return:
        """
        additional_args = {"market"}
        q = {"access_key": self.configure["access_key"],
             "coin_type": coin_type,
             "id": order_id,
             "extra": self._get_extra(additional_args, kargs)}
        return await self._query("cancel_order", q)

    async def get_account_info(self, **kargs):
        """

        :param kargs: Additional params for get_account_info.
        Please refer to: https://github.com/huobiapi/API_Docs/wiki/REST-get_account_info
        :return:
        """
        additional_args = {"market"}
        q = {"access_key": self.configure["access_key"],
             "extra": self._get_extra(additional_args, kargs)}
        return await self._query("get_account_info", q)

    async def get_orders(self, coin_type, **kargs):
        """

        :param coin_type: The type of the coin to buy. 1: BTC, 2: LTC.
        :param kargs: Additional params for get_orders.
        Please refer to: https://github.com/huobiapi/API_Docs/wiki/REST-get_orders
        :return:
        """
        additional_args = {"market"}
        q = {"access_key": self.configure["access_key"],
             "coin_type":coin_type,
             "extra": self._get_extra(additional_args, kargs)}
        return await self._query("get_orders", q)

    async def get_new_deal_orders(self, coin_type, **kargs):
        """

        :param coin_type: The type of the coin to buy. 1: BTC, 2: LTC.
        :param kargs: Additional params for get_new_deal_orders.
        Please refer to: https://github.com/huobiapi/API_Docs/wiki/REST-get_new_deal_orders
        :return:
        """
        additional_args = {"market"}
        q = {"access_key": self.configure["access_key"],
             "coin_type": coin_type,
             "extra": self._get_extra(additional_args, kargs)}
        return await self._query("get_new_deal_orders", q)

    async def get_order_id_by_trade_id(self, coin_type, trade_id, **kargs):
        """
        :param coin_type: The type of the coin to buy. 1: BTC, 2: LTC.
        param order_id: order id to request.
        :param kargs: Additional params for order_info.
        Please refer to: https://github.com/huobiapi/API_Docs/wiki/REST-order_info
        :return:
        """
        additional_args = {"market"}
        q = {"access_key": self.configure["access_key"],
             "id": trade_id,
             "extra": self._get_extra(additional_args, kargs)}
        return await self._query("get_order_id_by_trade_id", q)

    async def withdraw_coin(self, coin_type, withdraw_address, withdraw_amount, **kargs):
        """

        :param coin_type: The type of the coin to withdraw. 1: BTC, 2: LTC.
        :param withdraw_address:
        :param withdraw_amount: BTC>=0.01 LTC>=0.1
        :param kargs:Additional params for order_info.
        Please refer to: https://github.com/huobiapi/API_Docs/wiki/REST-withdraw_coin
        :return:
        """
        additional_args = {"trade_password", "withdraw_fee", "market"}
        q = {"withdraw_address": withdraw_address,
             "access_key": self.configure["access_key"],
             "withdraw_amount": withdraw_amount,
             "coin_type": coin_type,
             "extra": self._get_extra(additional_args, kargs)}
        return await self._query("withdraw_coin", q)

    async def cancel_withdraw_coin(self, withdraw_coin_id, **kargs):
        """
        param withdraw_coin_id: order id to cancel
        :param kargs: Additional params for order_info.
        Please refer to: https://github.com/huobiapi/API_Docs/wiki/REST-cancel_withdraw_coin
        :return:
        """
        additional_args = {"market"}
        q = {"access_key": self.configure["access_key"],
             "withdraw_coin_id": withdraw_coin_id,
             "extra": self._get_extra(additional_args, kargs)}
        return await self._query("cancel_withdraw_coin", q)

    async def get_withdraw_coin_result(self, withdraw_coin_id, **kargs):
        """
        param withdraw_coin_id: order id to cancel
        :param kargs: Additional params for order_info.
        Please refer to: https://github.com/huobiapi/API_Docs/wiki/REST-cancel_withdraw_coin
        :return:
        """
        additional_args = {"market"}
        q = {"access_key": self.configure["access_key"],
             "withdraw_coin_id": withdraw_coin_id,
             "extra": self._get_extra(additional_args, kargs)}
        return await self._query("get_withdraw_coin_result", q)

    async def order_info(self, coin_type, order_id, **kargs):
        """

        :param coin_type: The type of the coin to buy. 1: BTC, 2: LTC.
         param order_id: order id to request.
        :param kargs: Additional params for order_info.
        Please refer to: https://github.com/huobiapi/API_Docs/wiki/REST-order_info
        :return:
        """
        additional_args = {"market"}
        q = {"access_key": self.configure["access_key"],
             "id": order_id,
             "extra": self._get_extra(additional_args, kargs)}
        return await self._query("order_info", q)

    async def sell(self, amount, coin_type, price, **kargs):
        """

               :param amount: Total sell amount.
               :param coin_type: The type of the coin to buy. 1: BTC, 2: LTC.
               :param price: Sell at this price.
               :param kargs: Additional params for sell.
               Please refer to: https://github.com/huobiapi/API_Docs/wiki/REST-sell
               :return:
               """
        additional_args = {"trade_password", "trade_id", "market"}
        q = {"amount": amount,
             "access_key": self.configure["access_key"],
             "price": price,
             "coin_type": coin_type,
             "extra": self._get_extra(additional_args, kargs)}
        return await self._query("sell", q)

    async def sell_market(self, amount, coin_type,**kargs):
        """

        :param amount: Total sell amount.
        :param coin_type: The type of the coin to buy. 1: BTC, 2: LTC.
        :param kargs: Additional params for sell_market.
        Please refer to: https://github.com/huobiapi/API_Docs/wiki/REST-buy_market
        :return:
        """
        additional_args = {"trade_password", "trade_id", "market"}
        q = {"amount": amount,
             "access_key": self.configure["access_key"],
             "coin_type": coin_type,
             "extra": self._get_extra(additional_args, kargs)}
        return await self._query("sell_market", q)

    async def transfer(self, account_from, account_to, amount, coin_type=1):
        """

        :param account_from: 1: CNY account; 2: USD account
        :param account_to: 1: CNY account; 2: USD account
        :param amount: Amount to transfer.
        :param coin_type: 1: BTC
        :return:
        """
        q = {"amount": amount,
             "access_key": self.configure["access_key"],
             "coin_type": coin_type,
             "account_from": account_from,
             "account_to":account_to}
        return await self._query("transfer", q)

    def _get_extra(self, additional_args, source):
        return {k: source[k] for k in set(source.keys()).intersection(additional_args)}

    async def _query(self, method_name, params):
        if not self.trader:
            self.trader = HuobiAPI_LTC_BTC(secret_key=self.configure["secret_key"]).trade()
        raw = self.trader.__getattr__(method_name)(**params)
        query_param = {**raw,
                       "url": raw["url"] + "?" + raw["params"], }
        del query_param["params"]
        return await self.query(**query_param)

    async def process_response(self, response):
        return json.loads(response)
