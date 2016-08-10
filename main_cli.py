#!/usr/bin/python 
#-*- coding:utf-8 -*-

import random
import time
import timer
import sys
import engine
import http_client
import util
import debug
import json
import async_curl_module as ascurl

def main(data):
    conf = json.loads(data)
    host, port, nclients, interval, at_sec = conf["ip"], conf["port"], conf["clients"], conf["interval"], conf["at_sec"]    
    print host, port, nclients, interval, at_sec

    print ">>>>>>>>>>>>>connect start:", time.time()
    for i in range(nclients):
        wait = random.random() * 60
        url = "http://%s:%d/frontier_test/?id=%s_%d" % (host, port, util.getip().replace(".", "_"), i)
        timer.Timer().add(wait, http_client.request, (url, None, None, None))
    print "<<<<<<<<<<<<<connect end:", time.time()

if __name__ == '__main__':
    debug.isClient = True
    ascurl.get("http://127.0.0.1:6000/serviceinfo", main)
    engine.Engine().run()
