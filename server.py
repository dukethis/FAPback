#!/usr/bin/python3.7
# coding: utf-8

import os,sys,json,time,logging
import requests
from datetime import datetime,timedelta
from flask import Flask, request, redirect, render_template
from flask_restplus import Resource, Api, fields, reqparse

#====================
# INTERFACES IMPORT =
#====================

import index

#================
# CONFIGURATION =
#================

PARAMS = json.load( open("config.json","r") )
APP_NAME = PARAMS["APP"]
APP_DESC = PARAMS["DESCRIPTION"]
APP_VERSION = PARAMS["VERSION"]

HOST  = PARAMS["HOST"]
PORT  = PARAMS["PORT"]
DEBUG = PARAMS["DEBUG"]

#=================================
#========= APP CONFIG ============
#=================================

app = Flask( import_name=APP_NAME, template_folder='tpl')

# ACTUAL API
api = Api( app,
           title         = APP_NAME,
           version       = APP_VERSION,
           description   = APP_DESC,
           default       = 'CRUD',
           default_label = "Endpoints",
           prefix        = "",
           doc           = "/",
           validate      = False,
           ordered       = True)

#=========
# LOGGIN =
#=========

logging.basicConfig( level  = logging.DEBUG,
                     format = '%(asctime)-15s %(levelname)-7s %(message)s'
)
logger = logging.getLogger("werkzeug")

logger.setLevel(logging.DEBUG)
app.logger.setLevel(logging.WARNING)

START_TIME = datetime.now().strftime('%Y-%m-%d:%H:%M:%S')

#====================
# RESOURCES BINDING =
#====================

api.add_resource( index.Activities,  "/activities" )
api.add_resource( index.Activity,    "/activities/<int:index>" )

api.add_resource( index.Users,       "/users" )
api.add_resource( index.User,        "/users/<string:name>" )

api.add_resource( index.SaveContext, "/save" )

#=================================
#=========== FRONT END ===========
#=================================

@app.route("/home")
@app.route("/index")
def home():
    return "Flask Activity Pub Server is listening..."

#=================================
#========== MAIN RUN =============
#=================================

if __name__ == '__main__':
    app.run(host=HOST, port=PORT,debug=DEBUG)

