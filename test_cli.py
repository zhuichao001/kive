#!/usr/bin/python 
#-*- coding:utf-8 -*-

import sys
import socket
import json
import random
import struct

import config
import client
import engine

engine = engine.engine()

def build(ip, port):
    con = engine.connect(ip, port)
    engine.register(con, engine.receive, client.on_data)
    return con

def timeout(con):
    engine.send(con, client.req_headers("/", "10.4.43.155"))
    engine.addtimer(2, timeout, (con,))

def test():
    ip, port, clients, interval = config.get_config()
    for i in range(3):
        con = build(ip, port)
        engine.addtimer(1, timeout, (con,))
    engine.run()

if __name__ == '__main__':
    test()
