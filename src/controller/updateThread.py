#!/usr/bin/python
# -*- coding: utf-8 -*-

from threading import Thread, Event
from model import event2db
import datetime
import json

def startUpdater(config):
    stopFlag = Event()
    thread = Updater(stopFlag)
    thread.setConf(config)
    thread.start()

    return thread

class Updater(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event
        self.isUpdating = False

    def setConf(self, configPath):
        with open(configPath, 'r') as f:
            config = json.load(f)

            self.conf = config

    def run(self):
        self.loadDb()
        while not self.stopped.wait(1800.0):
            # call a function
            self.loadDb()

    def loadDb(self):
        self.isUpdating = True
        print ("{}: Refreshing Database".format(datetime.datetime.now()))
        event2db.loadDb(self.conf)
        print ("{}: Database Updated".format(datetime.datetime.now()))
        self.isUpdating = False

    def isUpdating(self):     
        return self.isUpdating

    def stop(self):
        self.stopped.set()
