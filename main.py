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
from handlers.group import NewgroupHandler,JoinGroupHandler,LeaveGroupHandler,GroupHandler
from handlers.people import PeopleHandler,RemoveFriendHandler,AddFriendHandler
from handlers.chat import ChatSocketHandler
from handlers.registration_login import LoginHandler,SignUpHandler,LogoutHandler,BaseHandler



define("port", default=9090, help="run on the given port", type=int)

x='ddd'
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/chatsocket", ChatSocketHandler),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
            (r'/signup', SignUpHandler),
            (r"/myhome", myhomeHandler),
            (r"/about", aboutHandler),
            (r"/group", GroupHandler),
            (r"/people", PeopleHandler),
            (r'/newgroup', NewgroupHandler),
            (r'/joingroup', JoinGroupHandler),
            (r'/leavegroup', LeaveGroupHandler),
            (r'/addfriend', AddFriendHandler),
            (r'/removefriend', RemoveFriendHandler)
            #(r"/chat", ChatHandler),
            #(r"/ws", WSHandler)
            #(r'/single', SingleChatHandler)


        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class myhomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("myhome.html")

    def post(self):
       pass



class aboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("about.html")

    def post(self):
       pass

        
class MainHandler(BaseHandler):
    def get(self):
       # x = ""
        new_values=dict()
        single = self.get_argument('single', None)
        if single:
            new_values['single'] = single
            global x 
            x= single[4:]
        print(x)
#        if self.get_current_user():
#            self.render("index.html", messages=ChatSocketHandler.cache)
        if self.get_current_user():
            self.render("ui_home.html", messages=ChatSocketHandler.cache)

            #self.render("ui_home.html", messages=ChatSocketHandler.cache)
        else:
#           self.redirect(u"/login")
            self.render("index.html")

def main():
    print("\n\tsever starting at localhost:9090")
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\n\tShutting server down")
        tornado.ioloop.IOLoop.instance().stop()

if __name__ == "__main__":
    main()
