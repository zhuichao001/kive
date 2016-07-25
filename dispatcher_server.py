#!/usr/bin/python 
#-*- coding:utf-8 -*-

import sys
import socket
import json
import random
import struct
import server
import gvar

def on_http_data(fd, http_req):
    e = gvar.Engine()
    if gvar.Debug:
        print "body:", http_req
    gvar.Engine().status.msgs += 1

    url = http_req[:http_req.find("\r\n")].split(" ")[1]
    if gvar.Debug:
        print fd, url
    id = url[url.rfind("=")+1:]
    if gvar.Debug:
        print "id:", id
    e.status.add_remote(fd, id)

    e.send_delay(fd, server.response(url), 0.001)


def on_data(fd, data):
    def on_socket_data(data):
        if not data.endswith("\r\n\r\n"):
            return 0
        on_http_data(fd, data)
        return len(data)

    if gvar.Debug:
    	print "--------------->>>>>>data:\n"
    	print data
    	print "------------------------"

    length = on_socket_data(data)
    return length
