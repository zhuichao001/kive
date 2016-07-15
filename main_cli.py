#!/usr/bin/python 
#-*- coding:utf-8 -*-

import sys
import socket
import json
import random
import struct

import getconfig
import engine
import gvar
import http_protocol
import util
import traceback

ip = util.getip().replace(".", "_")

def timeout(fd):
    try:
        url = "/frontier_test/?id=%s_%d" % (ip, fd)
        gvar.Engine().send(fd, http_protocol.req_headers(url, "10.4.43.155"))
    except:
        print "err fd=", fd
        traceback.print_exc()        
        pass

ip, port, clients, interval = getconfig.getconfig()
left = clients


#left = 1
#interval =1

def cycle():
    n = 0
    global left
    for i in range(left)[:20000]:
        fd = gvar.Engine().connect(ip, port)
        gvar.Engine().addtimer(random.random()*interval*2, timeout, (fd,))
        n += 1
    left -= n
    if n!=0:
        gvar.Engine().addtimer(1, cycle, ())
 

def main_old():
    ip, port, clients, interval = getconfig.getconfig()
    #ip, port = "10.4.43.155", 6000
    clients, interval = 50000, 10
    left = clients
    #clients, interval = 1, 2
    for i in range(clients):
        try:
            con = gvar.Engine().connect(ip, port)
            gvar.Engine().addtimer(random.random()*interval*2, timeout, (con,))
        except:
            pass
    gvar.Engine().run()


if __name__ == '__main__':
    gvar.SetEngine(engine.engine())
    cycle()
    gvar.Engine().run()
