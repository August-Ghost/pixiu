# -*- coding: utf-8 -*-
from base import baseinterface
from logsys.logger import get_logger


class ECInterface(baseinterface.BaseInterface):
    Interface_logger = None

    @classmethod
    def setlogger(cls):
        if cls.Interface_logger is None:
            cls.Interface_logger = get_logger("ECInterface")

    def __init__(self, **log_config):

        type(self).setlogger()
        self.logger = type(self).Interface_logger if not log_config \
            else type(self).Interface_logger.getChild(**log_config)
        super(ECInterface, self).__init__()
        self.init()

    def init(self):
        pass

    async def on_success(self, response):
        msg="{url} - {status}".format(url=response.effective_url.encode("utf-8"),
                                      status=response.code)
        self.logger.debug(msg)

    async def on_failure(self, error):
        msg = "{err} - {context}".format(err=error,
                                         context=self.request_params)
        self.logger.error(msg)
