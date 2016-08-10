#!/usr/bin/python 
#-*- coding:utf-8 -*-

import random
import time
import timer
import engine
import getconfig
import http_client
import util
import debug

def main():
    host, port, nclients, interval, at_sec = getconfig.getconfig()
    print host, port, nclients, interval, at_sec
    print ">>>>>>>>>>>>>connect start:", time.time()
    for i in range(nclients):
        wait = random.random() * 60
        url = "http://%s:%d/frontier_test/?id=%s_%d" % (host, port, util.getip().replace(".", "_"), i)
        timer.Timer().add(wait, http_client.request, (url, None, None, None))
    print "<<<<<<<<<<<<<connect end:", time.time()

if __name__ == '__main__':
    debug.isClient = True
    main()
    engine.Engine().run()
