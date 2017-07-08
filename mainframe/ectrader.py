# -*- coding: utf-8 -*-
from mainframe.configurable_query import ConfigurableQuery, REQUIRED
from logsys.logger import get_logger


class ECTrader(ConfigurableQuery):
    @classmethod
    def setlogger(cls):
        if cls.Query_logger is None:
            cls.Query_logger = get_logger("ECTrader")

    def init(self):
       self.trader = None
       self.checklist.update({"access_key": REQUIRED,
                              "secret_key": REQUIRED})
