# coding: utf-8 -*-
from base.baseclient import BaseClient
from mainframe.ecinterface import ECInterface
from logsys.logger import get_logger


OPTIONAL = lambda config: True
REQUIRED = lambda config: not not config


class ConfigurableQuery(BaseClient):
    Query_logger = None

    @classmethod
    def setlogger(cls):
        if cls.Query_logger is None:
            cls.Query_logger = get_logger("Query")


    def __init__(self):
        self.configure = {}
        self.checklist = {}

        self.init()
        self.config()
        self._validate()
        self.name = self.configure["name"]

        type(self).setlogger()
        super(ConfigurableQuery, self).__init__(interface=ECInterface(**{"name": self.name,
                                                                         **self.configure["interface_logging"]} if "interface_logging" in self.configure
                                                                      else {}))
        self.after_init()

    def init(self):
        """

        :return:
        """
        pass

    def after_init(self):
        """
         :return:
        """
        pass

    def config(self):
        pass

    def _validate(self):
        for config_path, validator in self.checklist.items():
            try:
                conf = self.config_getter(config_path.split("."), with_default=False)
            except KeyError as e:
                raise e
            else:
                if not validator(conf):
                    raise ValueError("{cp} is required, but not set.".format(cp=config_path))

    def config_getter(self, path, with_default=False, default=None):
        p = (path,) if isinstance(path, str) else path
        config_getter = lambda config, config_path: config if not config_path else config_getter(config[config_path[0]],
                                                                                                 config_path[1:])
        try:
            conf = config_getter(self.configure, p)
        except KeyError as e:
            if not with_default:
                raise e
            else:
                return default
        else:
            return conf

    async def query(self, **qurey_kargs):
        return await self.process_response((await super(ConfigurableQuery, self).query(**qurey_kargs)).body)

    async def process_response(self, response):
        return response