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



class AddFriendHandler(tornado.web.RequestHandler):
    def get(self):
        new_values=dict()
        lastmod = self.get_argument('lastmod', None)
        if lastmod:
            new_values['lastmod'] = lastmod
            print(lastmod)
            client = MongoClient()
            client = MongoClient('localhost', 27017)
            db = client.chat_database
            collection = db.test_collection
            users = db.users
            email = tornado.escape.json_decode(self.get_secure_cookie("email"))
            db.users.update({"email": email },{"$push":{ "Friends": lastmod[3:] }})
            self.render("/people")

    def post(self):
        pass

class RemoveFriendHandler(tornado.web.RequestHandler):
    def get(self):
        new_values=dict()
        last = self.get_argument('last', None)
        if last :
            new_values['last'] = last
            client = MongoClient()
            client = MongoClient('localhost', 27017)
            db = client.chat_database
            collection = db.test_collection
            users = db.users
            email = tornado.escape.json_decode(self.get_secure_cookie("email"))
            db.users.update({"email": email },{"$pull":{ "Friends": last }})
            self.render("/people")


    def post(self):
       pass
 


class PeopleHandler(tornado.web.RequestHandler):

    def get(self):
        # db.users.update({},{$set:{"Friends":["Ahmed","rana","ali"]} },false,true)
            friendList=[]
            usersList=[]
            #usersemailList=[]
            #useremail=""
            user=""
            client = MongoClient()
            client = MongoClient('localhost', 27017)
            db = client.chat_database
            collection = db.test_collection
            users = db.users
            email = tornado.escape.json_decode(self.get_secure_cookie("email"))
            user = tornado.escape.json_decode(self.get_secure_cookie("user"))

            for key , value in db.users.find_one({"email": email},{"_id":0 , "Friends":1}).items():
                for a in range(len(value)):
                    friendList.append(value[a])
            for  value  in db.users.find({},{"_id":0 , "Username":1,"email":1}):
                    if value['email']==email:
                        continue
                    usersList.append(value)
                    #usersemailList.append(value['email'])
                    print(value)
                    self.set_secure_cookie("friend", tornado.escape.json_encode(friendList))

            self.render("people.html",user=usersList,friends=friendList)


    def post(self):
        client.close()
