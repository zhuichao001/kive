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


def on_http_data(fd, http_body):
    print "body:", http_body
    #gvar.Engine().addtimer(6, lambda c: engine.send(c, http_protocol.req_headers("/", "10.4.43.155")), (fd,))

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
