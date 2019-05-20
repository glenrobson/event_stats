#!/usr/bin/python
import sys
import sqlite3
import os
import json
from bottle import Bottle
from bottle import route, run, template,debug, get, post, static_file, request, redirect, response
from gottingen import gottingen
sys.path.append('src')
import updateThread
from __init__ import setThreadInstance

rootApp = Bottle()
@rootApp.route('/')
@rootApp.route('/index.html')
def index():
    return template('src/view/index.tpl')

@rootApp.get("/favicon.ico")
def favicon():
    return static_file('favicon.ico', root="src/view/static/img/")

@rootApp.get("/static/<filepath:path>")
def files(filepath):
    return static_file(filepath, root="src/view/static")

if __name__ == "__main__":
    updateThreadObj = updateThread.startUpdater('conf/gottingen.json')
    setThreadInstance(updateThreadObj)
    rootApp.merge(gottingen)
    rootApp.run(debug=True, host='0.0.0.0', port=9000)
    updateThreadObj.stop()
