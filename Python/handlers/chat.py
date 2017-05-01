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




class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    #abosedek = 12
    waiters = []
    cache = []
    cache_size = 200
   #db.users.find({},{"_id":0 ,"email":1}):
               
    def check_origin(self, origin):
        return True


    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        user_json = self.get_secure_cookie("user")
        new_user = {}
        new_user['id'] = id(self)
        new_user['name'] = tornado.escape.json_decode(user_json)
        new_user[tornado.escape.json_decode(user_json)] = self
        ChatSocketHandler.waiters.append(new_user)

        print(ChatSocketHandler.waiters)


    def on_close(self):
        """ when websocket close, remove connection from waiters"""

        user_json = self.get_secure_cookie("user")
        #ChatSocketHandler.waiters[tornado.escape.json_decode(user_json)]
        ChatSocketHandler.waiters = [ d for d in ChatSocketHandler.waiters if d.get('id') != id(self)]
       

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]
    def on_message(self, message):
        user_json = self.get_secure_cookie("user")
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        chat = {
            "id": str(uuid.uuid4()),
            "body": parsed["body"],
            "user" : tornado.escape.json_decode(user_json)
            }
        
        logined_users = [v for d in ChatSocketHandler.waiters for k,v in d.items() if k=='name']
        print(logined_users),
        chat['logined_users'] = str(logined_users)
        
        ChatSocketHandler.update_cache(chat)
        #ChatSocketHandler.send_updates(chat)

        #sending message to all socket connections
        logging.info("sending message to %d waiters", len(ChatSocketHandler.waiters))
        for waiter in ChatSocketHandler.waiters:
            try:
            	current_user =  waiter['name'] 
            	
            	chat['current_user'] = current_user
            	chat["html"] = tornado.escape.to_basestring(
                  self.render_string("message.html", message=chat))
            	
            	
            	waiter[current_user].write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)
