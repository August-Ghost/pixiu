# -*- coding: utf-8 -*-
from mainframe.configurable_query import ConfigurableQuery, REQUIRED
from logsys.logger import get_logger


class ECDataSource(ConfigurableQuery):
    @classmethod
    def setlogger(cls):
        if cls.Query_logger is None:
            cls.Query_logger = get_logger("ECDataSource")

    def __init__(self):
        super(ECDataSource, self).__init__()
        self.logger = type(self).Query_logger if "datasource_logging" not in self.configure \
            else type(self).Query_logger.getChild(self.name, **self.configure["datasource_logging"])


    def init(self):
        self.checklist.update({"query_config": REQUIRED,
                               "name": REQUIRED,})

    async def __call__(self, **kargs):
        q = {**self.configure["query_config"],
             **kargs}
        return await self.query(**q)

    async def on_query_succeed(self, reply):
        self.logger.debug("{replay}".format(replay=reply.body))

    async def on_qurey_failed(self, err):
        self.logger.error("An error occurred: {e}".format(e=err))