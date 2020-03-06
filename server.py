#!/usr/bin/env python
# Copyright 2013 Abram Hindle
# Copyright 2019 Hazel Victoria Campbell
# Copyright 2020 Justin Liew
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask

import flask
from flask import Flask, request, redirect, send_from_directory
import json
app = Flask(__name__)
app.debug = True

class World:
    
    def __init__(self):
        self.clear()
        #self.space = dict()
        #self.listeners = dict()
        
    def update(self, entity, key, value):
        entry = self.space.get(entity,dict())
        entry[key] = value
        self.space[entity] = entry

    def set(self, entity, data):
        self.space[entity] = data
        self.notify_all(entity,data)

    def clear(self):
        self.space = dict()
        self.listeners = dict()

    def get(self, entity):
        return self.space.get(entity,dict())
    
    def world(self):
        return self.space

    def notify_all(self,entity,data):
        for listener in self.listeners:
           self.listeners[listener][entity] = data

    def add_listener(self,listener_name):
        #self.listeners[listener_name] = dict()
        self.listeners[listener_name] = self.space.copy()

    def get_listener(self, listener_name):
        return self.listeners[listener_name]

    def clear_listener(self, listener_name):
        self.listeners[listener_name] = dict()

# you can test
# curl -v   -H "Content-Type: appication/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}' 

myWorld = World()          

def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data != ''):
        return json.loads(request.data)
    else:
        return json.loads(request.form.keys()[0])

@app.route("/")
def hello():
    return redirect("/static/index.html", code=302)

@app.route("/entity/<entity>", methods=['POST','PUT']) 
def add_entity(entity):
    v = flask_post_json()
    myWorld.set( entity, v ) # notify_all is built into set
    e = myWorld.get(entity)    
    # flask has a security restriction in jsonify
    #return json.dumps( e ) # flask.jsonify( e )
    return flask.jsonify(e)

@app.route("/entity/<entity>")   ### when method unspecified, defaults to GET
def get_entity(entity):
    '''This is the GET version of the entity interface, return a representation of the entity'''
    e = myWorld.get(entity)
    #return json.dumps( e ) # flask.jsonify( e )
    return flask.jsonify(e)

@app.route("/listener/<entity>", methods=['POST','PUT']) # register id
def add_listener(entity):
    # don't i have to get the current state of the world on registration???
    # without, would it just get stuff drawn since new browser was open???
    # should probably modify add_listener to set listener bucket to the current world (on server)
    myWorld.add_listener( entity )
    return flask.jsonify(dict())

@app.route("/listener/<entity>")  ### GET
def get_listener(entity):
    v = myWorld.get_listener(entity)
    myWorld.clear_listener(entity)
    #print(v)
    return flask.jsonify( v ) # return items that need to be updated


@app.route("/world", methods=['POST','GET'])    
def world():
    '''you should probably return the world here'''
    w = myWorld.world()
    return flask.jsonify( w )


@app.route("/clear", methods=['POST','GET'])
def clear():
    '''Clear the world out!'''
    myWorld.clear()
    w = myWorld.world()
    return flask.jsonify( w )

'''
# what is this??????
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('js', path)
'''

if __name__ == "__main__":
    app.run()