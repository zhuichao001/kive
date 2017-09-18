#!/usr/bin/python 
#-*- coding:utf-8 -*-

import sys
import socket
import json
import random
import struct
import http_server
import engine
import settings
from app import *


def on_http_data(fd, http_req):
    if settings.Debug:
        print "body:", http_req
    url = http_req[:http_req.find("\r\n")].split(" ")[1]
    if settings.Debug:
        print fd, url

    eng = engine.Engine()
    eng.status.msgs += 1
    eng.status.add_remote(fd, url)

    eng.send_delay(fd, app.serve(url), 0.0001)

def on_socket_data(fd, data):
    if not data.endswith("\r\n\r\n"):
        return 0
    on_http_data(fd, data)
    return len(data)

def on_data(fd, data):
    if settings.Debug:
    	print "--------------->>>>>>data:\n"
    	print data
    	print "------------------------"
    length = on_socket_data(fd, data)
    return length
