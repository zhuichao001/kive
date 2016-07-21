#!/usr/bin/python 
#-*- coding:utf-8 -*-

import sys
import socket
import json
import random
import time
import getconfig
import engine
import gvar
import http_protocol
import util
import traceback

def con_send():
    fd = gvar.Engine().connect(gvar.host, gvar.port)
    if fd<0:
        print "Connect fd=-1"
        wait = random.random()*interval*2
        gvar.Engine().addtimer(wait, con_send, ())
        return
    gvar.Engine().send_nodelay(fd, http_protocol.req_data(fd))

def main():
    fds = []
    print ">>>>>>>>>>>>>connect start:", time.time()
    for i in range(gvar.clients):
        wait = random.random()*60
        gvar.Engine().addtimer(wait, con_send, ())
    print "<<<<<<<<<<<<<connect end:", time.time()

if __name__ == '__main__':
    gvar.host, gvar.port, gvar.clients, gvar.interval, gvar.at_sec = getconfig.getconfig()
    print gvar.host, gvar.port, gvar.clients, gvar.interval, gvar.at_sec
    gvar.SetEngine(engine.engine())
    main()
    gvar.Engine().run()
