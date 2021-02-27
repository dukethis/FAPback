#!/usr/bin/python3
# coding: UTF-8
#=================================
#=========== IMPORTS =============
#=================================
import os,json,datetime,requests
from flask import request,Response
from flask_restplus import Resource

#=================================
#============ PARAMS =============
#=================================

PARAMS = json.load( open("config.json","r") )
HOST   = PARAMS["HOST"]+":"+str(PARAMS["PORT"])

ROUTES = {
    "Actor"    : "users",
    "Person"   : "users",
    "Service"  : "users",
    "Activity" : "activities",
}

SCHEME = "http://"

#=================================
#=========== CLASSES =============
#=================================


class Object:
    def __init__(self, **kargs):
        self.context = "https://www.w3.org/ns/activitystreams"
        self.type    = "Object"
        self.__dict__.update( kargs )
        if self.type.title() in ROUTES.keys():
            print(f"FOUND  TYPE {self.type}")
        if "context" in self.__dict__.keys():
            print(f"CONTEXT TYPE {self.type}")
            url = self.context
            if type(url)==dict and"type" in url.keys():
                req = requests.request("HEAD", url["type"], headers={"User-Agent":"FAP/0.1"})
                if req.status_code != 200:
                    return None

    def __str__(self):
        return json.dumps(self.__dict__, default=lambda x: x.__dict__, indent=2)

class Actor(Object):
    def __init__(self, **kargs):
        kargs["type"] = kargs["type"] if "type" in kargs.keys() else "Actor"
        Object.__init__(self, **kargs )
        self.id = SCHEME + "/".join( [ HOST , ROUTES[ "Actor" ] , self.name ] )


class Activity(Object):
    count = 1
    def __init__(self, **kargs):
        kargs["type"] = kargs["type"] if "type" in kargs.keys() else "Activity" 
        Object.__init__(self, **kargs )
        self.index = int(Activity.count)
        # BUILD SELF ID
        self.id = SCHEME + "/".join( [ HOST , ROUTES[ "Activity" ] , str(self.index) ] )
        # INCREMENT COUNTER
        Activity.count += 1
        print(self)

class Collection(list):
    def __init__(self, items=[], **kargs):
        if "names" in kargs.keys():
            print( kargs )
        elif not isinstance(items,list):
            raise TypeError("Mandatory argument is a list of items")
        elif not all([ isinstance(x,Object) for x in items ]):
            raise TypeError("Mandatory argument is a list of Object items")
        list.__init__(self, items )
        self.type = "Collection"
        self.items = self

    def __str__(self):
        return json.dumps(self.__dict__, default=lambda x: x.__dict__, indent=2)
        #~ return json.dumps( [ json.loads(u.__str__()) for u in self ], indent=2 )


