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

def main(host, port, clients, interval):
    localip = util.getip().replace(".", "_")
    fds = []
    print ">>>>>>>>>>>>>connect start:", time.time()
    for i in range(clients):
        fd = gvar.Engine().connect(host, port)
        if fd>0:
            fds.append(fd)

    for fd in fds:
        url = "/frontier_test/?id=%s_%d" % (localip, fd)
        gvar.Engine().send_delay(fd, http_protocol.req_headers(url, host), random.random()*interval*2)
    print "<<<<<<<<<<<<<connect end:", time.time()
 
if __name__ == '__main__':
    host, port, clients, interval, at_sec = getconfig.getconfig()
    gvar.SetEngine(engine.engine())
    gvar.abtimer(at_sec, main, (host, port, clients, interval))
    gvar.Engine().run()
