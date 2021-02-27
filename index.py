#!/usr/bin/python3
# coding: UTF-8
#=================================
#=========== IMPORTS =============
#=================================
import os,json,datetime,requests
from flask import request,Response
from flask_restplus import Resource
from objects import Activity as ACTIVITY
from objects import Actor as ACTOR
from objects import Collection

#=================================
#============ PARAMS =============
#=================================

PARAMS = json.load( open("config.json","r") )
HOST   = PARAMS["HOST"]+":"+str(PARAMS["PORT"])

#=================================
#========= API INTERFACE =========
#=================================

USERS = Collection( [] )

NOTES = Collection( [] )
# ACTIVITIES = Collection( [
#     {
#         "summary": "AP Server starts",
#         "type"   : "Object",
#         "id"     : f"{HOST}",
#         "object" : None
#     }
# ])

startTime = datetime.datetime.now()
startTime = datetime.datetime.strftime( startTime, "%Y-%m-%dT%H:%M:%S")

ACTIVITIES = Collection( [
    ACTIVITY(id=f"{HOST}", type="Event", name="ActivityPub backend server starts", startTime=startTime)
])

CONTEXT = { "activities":  ACTIVITIES.__dict__, "users": USERS.__dict__ }

FILENAME_CONTEXT = "context.json"

def SAVE_CONTEXT():
	get_context = { "activities":  ACTIVITIES.__dict__, "users": USERS.__dict__ }
	print( type(get_context["activities"]) )
	print( type(CONTEXT) )
	print(CONTEXT)
class User(Resource):
    def get(self, name):
        user = [ x for x in USERS if x.name == name.title() ]
        user = user[0].__dict__ if len(user)>0 else None
        return user,200

class Users(Resource):
    def get(self):
        users = [ a.__dict__ for a in USERS ]
        return users,200
    
    def post(self):
        data = request.json
        if not data:
            return {"Status 400":"Please provide a JSON content type"},400
        if any([ x in data.keys() for x in ["name","username","preferredUsername"] ]):
            actor = ACTOR( **data )
            if not any([ x.id == actor.id for x in USERS ]):
                USERS.append( actor )
            return actor.__dict__,200
        return {"Status":"Missing keys"},406


    
class Activities(Resource):
    def get(self):
        users = [ a.__dict__ for a in ACTIVITIES ]
        return users,200
    
    def post(self):
        """ Post a new activity	
        """
        data = request.json
        if not data:
            return {"Status 400":"Please provide a JSON content type"},400
        a = ACTIVITY( **data )
        print(a)
        if "type" in data.keys() and data["type"].title() in ["Activity","Event","Create","Note","Like"]:
            if not getattr(a,"id",None) or not any([ x.id == a.id for x in ACTIVITIES ]):
                ACTIVITIES.append( a )
            return a.__dict__,200
        return {"Status" : f"Missing keys: {','.join([ x.id == a.id or x.id for x in ACTIVITIES ])}"},406



class SaveContext(Resource):
	def get(self):
		SAVE_CONTEXT()
		return {"Status":"Data is saved"}
	
class Activity(Resource):
    def get(self,index):
        acts = [ a.__dict__ for a in ACTIVITIES if a.index == index ]
        acts = acts[0] if len(acts)>0 else None
        return acts,200
