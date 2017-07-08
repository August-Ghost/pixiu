# -*- coding:utf-8 -*-
from tornado import ioloop


class BaseStrategy:
    def __init__(self, datasource):
        self.name = id(self)
        self.datasource = datasource
        self.period = 0
        self.init()

    async def cold_start(self):
        """
        Will be called only once before the first time the strategy run.
        It is strongly recommended to 'warming up'  the indexes for the
        sake of accuracy.
        :return:
        """
        pass

    def __getattr__(self, item):
        """
        If an attribute not found in the usual places, this method will be called.
        I use this mechanism to allow strategy to refer to the datasources.
        :param item:
        :return:
        """
        try:
            attr = object.__getattribute__(self, "datasource")[item]
        except KeyError as e:
            raise AttributeError("No datasource named {0}".format(item))
        else:
            return attr

    def start(self):
        """
        Add strategy to ioloop.
        :return:
        """
        ioloop.IOLoop.current().add_callback(self.cold_start)
        if self.period:
            self.periodic_task = ioloop.PeriodicCallback(self._process, callback_time=self.period)
            self.periodic_task.start()
        else:
            ioloop.IOLoop.current().add_callback(self._process)

    def stop(self):
        if self.period:
            self.periodic_task.stop()

    def init(self):
        pass

    async def _process(self):
        try:
            await self.process()
        except Exception as e:
            self.on_error_occurred(e)
            raise e

    async def process(self):
        """
        Overwrite it with your strategy
        :return:
        """
        pass

    def on_error_occurred(self, err):
        """
        If any exception raised directly in your strategy, this method will be
        called with it.
        :param err:
        :return:
        """
        pass
