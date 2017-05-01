 #! /usr/bin/python3
from tornado import web,ioloop,gen
#import os, time
import logging
import os.path
import uuid
import pymongo
from bson.objectid import ObjectId
from pymongo import MongoClient
import tornado.escape
import tornado.websocket
from tornado.options import define, options
import json 

class NewgroupHandler(tornado.websocket.WebSocketHandler):

    def get(self):
        self.render("newgroup.html")

    def post(self):
        Groupname = self.get_argument("groupname", "")
        client = MongoClient()
        client = MongoClient('localhost', 27017)
        db = client.chat_database
        collection = db.test_collection
        email = tornado.escape.json_decode(self.get_secure_cookie("email"))
        group = { "Groupname": Groupname,"email":email}
        groups = db.groups
        group_id = groups.insert(group)
        client.close()
#        self.render("group.html")
        self.redirect(self.get_argument("next", u"/group")) 
   
class JoinGroupHandler(tornado.web.RequestHandler):
    def get(self):
        new_values=dict()
        joinG = self.get_argument('joinG', None)
        if joinG:
            new_values['joinG'] = joinG
            print(joinG)
            client = MongoClient()
            client = MongoClient('localhost', 27017)
            db = client.chat_database
            collection = db.test_collection
            users = db.users
            email = tornado.escape.json_decode(self.get_secure_cookie("email"))
            db.users.update({"email": email },{"$push":{ "Groups": joinG[3:] }})
            #db.users.update({"email": email },{"$push":{ "Groups": joinG }})
            self.render("/group")

    def post(self):
       pass


class LeaveGroupHandler(tornado.web.RequestHandler):
    def get(self):
        new_values=dict()
        leaveG = self.get_argument('leaveG', None)
        if leaveG :
            new_values['leaveG'] = leaveG
            print("leaveG"+leaveG)
            client = MongoClient()
            client = MongoClient('localhost', 27017)
            db = client.chat_database
            collection = db.test_collection
            users = db.users
            email = tornado.escape.json_decode(self.get_secure_cookie("email"))
            db.users.update({"email": email },{"$pull":{ "Group": leaveG[2:] }})
            self.render("/group")
       
 
class GroupHandler(tornado.web.RequestHandler):

    def get(self):
            groupList=[]
            MygroupList=[]
            MygroupListId=[]
            group=""
            mygroup=""
            client = MongoClient()
            client = MongoClient('localhost', 27017)
            db = client.chat_database
            collection = db.test_collection
            groups = db.groups
            email = tornado.escape.json_decode(self.get_secure_cookie("email"))
            for value in db.groups.find({"email": email},{"_id":1 , "Groupname":1}):
                    MygroupList.append(value['Groupname'])
                    print(value['Groupname'])
            for  value  in db.groups.find({},{"_id":1 , "Groupname":1}):
                    groupList.append(value)
                    print(value)
            for key , value in db.users.find_one({"email": email},{"_id":0 , "Groups":1}).items():
                for a in range(len(value)):
                    MygroupList.append(value[a])
            #for key , value in db.users.find_one({"email": email},{"_id":0 , "Groups":1}).items():
                ##for a in range(len(value)):
                    ###k=db.groups.find({"_id":'ObjectId('+value[a]+')'},{"_id":1, "Groupname":1})
                    ##k=value[a]
                    ##MygroupListId.append(value[a])
                    
                    ##print(k)
           # for key , value in MygroupListId:


            self.render("group.html",group=groupList,mygroup=MygroupList)
