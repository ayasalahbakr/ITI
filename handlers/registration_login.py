
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



class BaseHandler(tornado.web.RequestHandler):

    def get_login_url(self):
      return u"/login"

    def get_current_user(self):
        user_json = self.get_secure_cookie("user")

        if user_json:
           return tornado.escape.json_decode(user_json)
        else:
           return None



class LoginHandler(BaseHandler):
    auth=False
    client = MongoClient()
    client = MongoClient('localhost', 27017)
    db = client.chat_database
    exist=""
    username=""
    email='';
    user = {}

    def get(self):
        self.render("login_new.html", next=self.get_argument("next","/"))
        print (self.db.collection_names())

    def post(self):
        email = self.get_argument("email", "")
        password = self.get_argument("password", "")
        self.exist=self.db.users.find_one({"email": email})
        self.auth =self.check_auth(password, email)
        friends=""
      #  for friends in self.db.users.find_one({"email": email})['friends']:

            #print ("test test test"+self.db.users.find_one({"ObjectId": friends})['Username'])
        if self.auth==True:
            self.set_current_user(self.username,self.email)
            users = self.db.users
            self.user['status'] = 1
            self.db.users.update({"email": email }, {"$set": self.user}, upsert=False)
            self.redirect(self.get_argument("next", u"/"))
        elif self.auth==False:
            error_msg = u"?error=Login incorrect."
            self.redirect(u"/" + error_msg)


    def set_current_user(self, user,email):
        if email:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
            self.set_secure_cookie("email", tornado.escape.json_encode(email))

        else:
            self.clear_cookie("user")
            self.clear_cookie("email")

    def check_auth(self, password, email):
        if self.exist is not None:
            if password == self.db.users.find_one({"email": email})['password'] :
                self.username=self.db.users.find_one({"email": email})['Username']
                self.email=self.db.users.find_one({"email": email})['email']

                return True
        return False

   

class LogoutHandler(BaseHandler):
    client = MongoClient()
    client = MongoClient('localhost', 27017)
    db = client.chat_database
    user = {}
    def post(self):
        self.clear_cookie("user")
        email = tornado.escape.json_decode(self.get_secure_cookie("email"))
        self.user['status'] = 0
        self.db.users.update({"email": email }, {"$set": self.user}, upsert=False)
        #print(str(email))
        self.clear_cookie("user")

#       self.redirect("templates/index.html")
        self.redirect(u"/login")
      # self.render("/login")

    get = post

    get = post

class SignUpHandler(tornado.websocket.WebSocketHandler):

    def get(self):
        self.render("signup.html")

    def post(self):
        username = self.get_argument("username", "")
        email = self.get_argument("email", "")
        password = self.get_argument("password", "")

        client = MongoClient()
        client = MongoClient('localhost', 27017)
        db = client.chat_database
        collection = db.test_collection
        #If status is 0 the user is inactive, if 1 the user is active
        user = { "Username": username ,"email": email, "password": password ,'status' : 0}
        users = db.users
        user_id = users.insert(user)

        #print username,email,password
        obj_id = db.users.find_one({"Username": username})['_id']

        #to see saved usernames and passwords
        for post in users.find():
           print(post)
        client.close()
    #    self.render("rm.html")
        self.render("confirm.html")
         
