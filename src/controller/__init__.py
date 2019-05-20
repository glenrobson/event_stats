#!/usr/bin/python

from bottle import template

updateThreadObjIns = None
def setThreadInstance(threadObj):
    global updateThreadObjIns
    updateThreadObjIns = threadObj

def isDBReady():
    global updateThreadObjIns
    return updateThreadObjIns.isUpdating

def dbUpdating():  
    return template('src/view/databaseUpdating.tpl')

