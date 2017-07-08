# -*- coding: utf-8 -*-
from tornado import ioloop
from mainframe.shepherd import Shepherd



class Mainframe:
    def __init__(self):
        self.shepherd = Shepherd()
        self.ioloop = ioloop.IOLoop.current()

    def start(self):
        self.shepherd.shepherd()
        self.ioloop.start()

    def stop(self):
        self.shepherd.kill()
        self.ioloop.stop()
