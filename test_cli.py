#!/usr/bin/python 
#-*- coding:utf-8 -*-

import sys
import socket
import json
import random
import struct

import getconfig
import http_protocol
import engine

engine = engine.engine()

def build(ip, port):
    fd = engine.connect(ip, port)
    return fd

def timeout(fd):
    engine.send(fd, http_protocol.req_headers("/", "frontier.snssdk.com"))
    engine.addtimer(2, timeout, (fd,))

def test():
    ip, port, clients, interval, at_sec = getconfig.getconfig()
    for i in range(3):
        fd = build(ip, port)
        engine.addtimer(1, timeout, (fd,))
    engine.run()

if __name__ == '__main__':
    test()
