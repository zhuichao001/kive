#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
import kive.config.settings as settings
import kive.http.http_client as http_client

callbacks = {}

def register(fd, callback):
    global callbacks
    callbacks[fd] = callback

def on_http_data(fd, http_body):
    print "on_http_data is called"
    callback=callbacks.get(fd)
    if callback != None:
        print "callback(),  is called"
        callback(fd, http_body)
    else:
        print "http_client.response(),  is called"
        http_client.response(fd, http_body)

def on_socket_data(fd, data):
    if not data.endswith("\r\n0\r\n\r\n"):
        if settings.Debug:
            print >>sys.stderr, "WARNING||||||socket data:", data
        return 0
    blocks = data.split("\r\n\r\n")
    body = blocks[1][:]
    idx = body.find("\r\n")
    body = body[idx+2:]
    on_http_data(fd, body)
    return len(data)

def on_data(fd, data):
    if settings.Debug:
        print "--------------->>>>>>data:\n"
        print data
        print "<<<<<<--------------------"
    length = on_socket_data(fd, data)
    return length
