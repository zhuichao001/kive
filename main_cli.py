#!/usr/bin/python 
#-*- coding:utf-8 -*-

import random
import time
import getconfig
import http_client
import gvar
import util

def main():
    print ">>>>>>>>>>>>>connect start:", time.time()
    for i in range(gvar.clients):
        wait = random.random()*60
        url = "http://%s:%d/frontier_test/?id=%s_%d" % (gvar.host, gvar.port, util.getip().replace(".", "_"), i)
        gvar.Timer().add(wait, http_client.request, (url, None, None, None))
    print "<<<<<<<<<<<<<connect end:", time.time()

if __name__ == '__main__':
    gvar.host, gvar.port, gvar.clients, gvar.interval, gvar.at_sec = getconfig.getconfig()
    print gvar.host, gvar.port, gvar.clients, gvar.interval, gvar.at_sec

    main()
    gvar.Engine().run()
