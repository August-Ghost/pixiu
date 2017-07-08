# -*- coding: utf-8 -*-
import logging
from os.path import join


LOGGER_INSTANCE = {}
logging.getLogger().addHandler(logging.NullHandler())


def get_logger(name, logger=None, **kargs):
    if name not in LOGGER_INSTANCE:
        LOGGER_INSTANCE[name] = Logger(name, logger, **kargs)
    return LOGGER_INSTANCE[name]


def getHandler(hdlr_cls, lvl=logging.DEBUG, format=None, *args, **kargs):
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s" if not format \
                                      else format)
    hdlr = hdlr_cls(*args, **kargs)
    hdlr.setFormatter(formatter)
    if lvl:
        hdlr.setLevel(lvl)
    return hdlr

def getFileHandler(logfile, lvl=logging.DEBUG, format=None):
    return getHandler(logging.FileHandler, lvl, format, logfile)


class Logger:
    Logger_config = {}
    Logger_rootlogger = logging.getLogger("Pixiu")

    @classmethod
    def configure(cls,**kargs):
        cls.Logger_config.update(kargs)
        if kargs.get("if_verbose", False):
            cls.Logger_rootlogger.addHandler(getHandler(logging.StreamHandler,
                                                        lvl=logging.DEBUG))
        cls.Logger_rootlogger.setLevel(logging.DEBUG if kargs.get("if_debug", False)
                                       else logging.ERROR)

    @property
    def rootlogger(self):
        return type(self).Logger_rootlogger

    def __init__(self, name, logger=None, **kargs):
        self.name = name
        self.config = {**type(self).Logger_config, **kargs}
        self.logger = type(self).Logger_rootlogger.getChild(name) if not logger\
            else logger
        self._logger_setup()
        if not logger:
            self.logger.setLevel(logging.DEBUG if self.config.get("if_debug", False)
                                 else logging.ERROR)

    def _logger_setup(self):
        if self.config.get("if_debug", False):
            if not self.config.get("if_verbose", False):
                self.logger.addHandler(getHandler(logging.StreamHandler,
                                                  lvl=logging.DEBUG))

            dbglog = self.config.get("dbglog", "") or join(self.config.get("loghome", "log"),
                                          "{name}_debug.log".format(name=self.name))
            self.logger.addHandler(getFileHandler(dbglog, logging.DEBUG))

        errlog = self.config.get("errlog", "") or join(self.config.get("loghome", "log"),
                                      "{name}_error.log".format(name=self.name))
        self.logger.addHandler(getFileHandler(errlog, logging.ERROR))

    def __getattr__(self, item):
        return object.__getattribute__(object.__getattribute__(self, "logger"), item)

    def getChild(self, name, **kargs):
        return LOGGER_INSTANCE.setdefault('.'.join((self.name, name)),
                                          Logger(name='.'.join((self.name, name)), **kargs))

