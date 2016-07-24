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
from urlparse import urlsplit

callbacks = {}

def request(url, post=None, headers=None, callback=None):
    res = urlsplit(url)
    if res.scheme != "http":
        print "Exception, temperarily not support ", res.scheme
        return
    host, port = res.netloc, 80
    idx = res.netloc.find(':')
    if idx>0:
        host, port =  res.netloc[:idx], int(res.netloc[idx+1:])
    url = res.path
    fd = gvar.Engine().connect(host, port)
    if fd<0:
        print "Connect fd=-1"
        wait = random.random()*interval*2
        gvar.Engine().addtimer(wait, request, (url, post, headers, callback))
        return
    callbacks[fd] = callback
    gvar.Engine().send_nodelay(fd, http_protocol.req_headers(url, host))


def on_http_data(fd, http_body):
    callback=callbacks.get(fd)
    if callback != None:
        callback(fd, http_body)
    else:
        print "MSG:", http_body
#gvar.Engine().send_delay(fd, http_protocol.req_data(fd), gvar.interval)

def on_data(fd, data):
    def on_socket_data(data):
        if not data.endswith("\r\n0\r\n\r\n"):
            return 0
        blocks = data.split("\r\n\r\n")
        body = blocks[1][:]
        idx = body.find("\r\n")
        length = int(body[:idx],16)
        body = body[idx+2:]
        on_http_data(fd, body)
        return len(data)

    if gvar.Debug:
    	print "--------------->>>>>>data:\n"
    	print data
    	print "------------------------"

    length = on_socket_data(data)
    return length
