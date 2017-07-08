# -*- coding: utf-8 -*-
from os.path import basename, split, dirname, splitext
from glob import iglob
from logsys.logger import get_logger


class Shepherd:
    Shepherd_error_log = None

    def __init__(self):
        if type(self).Shepherd_error_log is None:
            type(self).Shepherd_error_log = get_logger(name="syslog")
        self.datasource_home = dirname(__import__("datasource").__file__)
        self.strategy_home = dirname(__import__("strategy").__file__)
        self.datasource = {}
        self.strategy = {}


    def get_module(self, module_path, excluded="__init__.py"):

        excluded = set("{0}.{1}".format(split(module_path)[1], splitext(basename(ex))[0])
                       for ex in ({excluded} if isinstance(excluded, str) else set(excluded)))

        return set("{0}.{1}".format(split(module_path)[1], splitext(basename(path))[0])
                     for path in iglob("{0}/*.py".format(module_path))) - excluded

    def shepherd(self):
        # Build datasource
        for dts_moudule in self.get_module(self.datasource_home):
            try:
                prototype = __import__(dts_moudule,
                                       globals(),
                                       locals(),
                                       ["EXPORT"],)
            except Exception as e:
                type(self).Shepherd_error_log.error(e)
            else:
                if not hasattr(prototype, "EXPORT"):
                    continue
                else:
                    dts = prototype.EXPORT()
                    self.datasource[dts.name] = dts

        for strategy_module in self.get_module(self.strategy_home):
            try:
                prototype = __import__(strategy_module,
                                       globals(),
                                       locals(),
                                       ["EXPORT"],)
            except Exception as e:
                type(self).Shepherd_error_log.error(e)
            else:
                if not hasattr(prototype, "EXPORT"):
                    continue
                else:
                    strategy = prototype.EXPORT(self.datasource)
                    self.strategy[strategy.name] = strategy

        for strategy in self.strategy.values():
            strategy.start()

    def kill(self):
        for strategy in self.strategy.values():
            strategy.stop()
