from trader.huobi_trader import Huobi_Trader

class Huobi_test_trader(Huobi_Trader):
    def config(self):
        self.configure = {
            "access_key": "your access_key",
            "secret_key": "your secret_key",
        }