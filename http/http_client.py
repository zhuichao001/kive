#!/usr/bin/python 
#-*- coding:utf-8 -*-

import random
from urlparse import urlsplit
import kive.event.timer as timer
import kive.event.engine as engine
import kive.http.http_protocol as http_protocol
import kive.http.dispatcher_client as dispatcher_client

def request(url, post=None, headers=None, callback=None):
    res = urlsplit(url)
    if res.scheme != "http":
        print "Exception, temperarily not support ", res.scheme
        return
    host, port = res.netloc, 80
    idx = res.netloc.find(':')
    if idx>0:
        host, port =  res.netloc[:idx], int(res.netloc[idx+1:])
    half_url = url[url.index(res.netloc)+len(res.netloc):]

    fd = engine.Engine().connect(host, port)
    if fd<0:
        print "Connect fd=-1"
        wait = random.random()*interval*2
        timer.Timer().add(wait, request, (url, post, headers, callback))
        return
    dispatcher_client.register(fd, callback)
    engine.Engine().send_nodelay(fd, http_protocol.req_headers(half_url, host))

def response(fd, data):
        print  "MSG[fd=%d]:%s" % (fd, data)
