# -*- coding: utf-8 -*-
from tornado.httpclient import AsyncHTTPClient
from docopt import docopt
from mainframe.mainframe import Mainframe
from logsys.logger import Logger, get_logger, getHandler
from os.path import abspath, join
import signal
import logging


__doc__ = "".join((
    """
    Pixiu is an non-blocking electronic currency quantitative trading system.
    """,
    """
    Usage:
    pixiu.py [-h | --help]
    pixiu.py start [-d | --debug ][-l | --syslog <syslog>][-v | --verbose][--loghome <loghome>][--pycurl]
    pixiu.py traceback [-d | --debug ][-l | --syslog <syslog>][-v | --verbose][--loghome <loghome>][--pycurl]
    pixiu.py create datasource <name> <dst>
    pixiu.py create strategy <name> <dst>
    """,
    """
    Options:
    -h --help    Show help message.
    -d --debug    Debug flag. Set if debug info is desired. Default to False. [default: False]
    -l --syslog <syslog>     Set system log file.
    -v --verbose    Set if logging to stdout is needed.
    --pycurl    Set if tornado.curl_httpclient.CurlAsyncHTTPClient is preferred.
    --loghome <loghome>    Set the path to store logs. [default: ./log]
    start   Start system in normal mode.
    traceback Start system in traceback mode(coming soon).
    create datasource <name> <dst> Create a datasource from template in current.
    create strategy <name> <dst> Create a strategy from template in destination.
    """
))

def create(name, template_file, dst):
    from string import Template
    with open(template_file, "r") as t:
        template = Template(t.read())
        with open(join(dst, "{0}.py".format(name)), "w") as d:
            d.write(template.safe_substitute(name=name))




if __name__ == "__main__":
    from docopt import DocoptExit
    arguments = docopt(__doc__)

    Logger.configure(if_debug=arguments.get("--debug", False),
                     if_verbose=arguments.get("--verbose", False),
                     loghome=arguments.get("--loghome", abspath("log")))

    l = get_logger(name="syslog",
                   logger=logging.getLogger("tornado.application"),
                   errlog="log/sys.log")
    if arguments.get("--verbose", False):
        l.addHandler(getHandler(logging.StreamHandler, lvl=logging.ERROR))

    if arguments.get("--pycurl", False):
        AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

    if arguments.get("start", False):
        mainframe = Mainframe()
        mainframe.start()
        signal.signal(signal.SIGINT, mainframe.stop)
        signal.signal(signal.SIGTERM, mainframe.stop)

    elif arguments.get("create", False):
        if arguments.get("datasource", False):
            create(name=arguments["<name>"],
                   template_file="utilities/datasource.template",
                   dst=arguments["<dst>"])
            print("A new datasource created in {0}.".format(abspath(arguments["<dst>"])))
        elif arguments.get("strategy", False):
                create(name=arguments["<name>"],
                       template_file="utilities/strategy.template",
                       dst=arguments["<dst>"])
                print("A new strategy created in {0}.".format(abspath(arguments["<dst>"])))
        else:
            raise DocoptExit

    elif arguments.get("traceback", False):
        print("Coming soon :)")

    else:
        raise DocoptExit
