#!/usr/bin/python 
#-*- coding:utf-8 -*-

import sys
import socket
import json
import random
import struct

import kive.http.http_protocol as http_protocol
import kive.event.engine as engine

engine = engine.engine()

def build(ip, port):
    fd = engine.connect(ip, port)
    return fd

def timeout(fd):
    engine.send(fd, http_protocol.req_headers("/", "frontier.snssdk.com"))
    engine.addtimer(2, timeout, (fd,))

def test():
    ip, port, clients, interval = "0.0.0.0", 6000, 10, 1
    for i in range(3):
        fd = build(ip, port)
        engine.addtimer(1, timeout, (fd,))
    engine.run()

if __name__ == '__main__':
    test()
