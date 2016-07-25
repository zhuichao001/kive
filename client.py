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
import dispatcher_client


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
    dispatcher_client.register(fd, callback)
    gvar.Engine().send_nodelay(fd, http_protocol.req_headers(url, host))

def response(fd, data):
        print  "MSG[fd=%d]:%s" % (fd, data)
        #gvar.Engine().send_delay(fd, http_protocol.req_data(fd), gvar.interval)
