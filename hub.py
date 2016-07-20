#!/usr/bin/python 
#-*- coding:utf-8 -*-

import sys
import socket
import json
import random
import struct
import client
import gvar
import http_protocol


def sendResponse(fd):
    e = gvar.Engine()
    response = http_protocol.responseData("[Keep-Alive Test connections=%d, msgs=%d, qps=%d, max_qps=%d]" % (e.status.n, e.status.msgs, e.status.qps, e.status.max_qps))
    if gvar.Debug:
        print "sendResponse:", response
    e.send_delay(fd, response, 0.001)

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

    sendResponse(fd)


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
