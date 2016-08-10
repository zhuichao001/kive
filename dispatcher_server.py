#!/usr/bin/python 
#-*- coding:utf-8 -*-

import sys
import socket
import json
import random
import struct
import http_server
import engine
import debug

def on_http_data(fd, http_req):
    eng = engine.Engine()
    if debug.Debug:
        print "body:", http_req
    eng.status.msgs += 1

    url = http_req[:http_req.find("\r\n")].split(" ")[1]
    if debug.Debug:
        print fd, url

    id = url[url.rfind("=")+1:]
    if debug.Debug:
        print "id:", id
    eng.status.add_remote(fd, id)

    eng.send_delay(fd, http_server.response(url), 0.0001)

def on_socket_data(fd, data):
    if not data.endswith("\r\n\r\n"):
        return 0
    on_http_data(fd, data)
    return len(data)

def on_data(fd, data):
    if debug.Debug:
    	print "--------------->>>>>>data:\n"
    	print data
    	print "------------------------"
    length = on_socket_data(fd, data)
    return length
