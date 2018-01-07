#!/usr/bin/python 
#-*- coding:utf-8 -*-

import random
import time
import json
import kive.event.timer as timer
import kive.event.engine as engine
import kive.http.http_client as http_client
import kive.common.util as util
import kive.config.settings as settings
import async_curl as ascurl

def start(data):
    conf = json.loads(data)
    host, port, nclients, interval, at_sec = conf["ip"], conf["port"], conf["clients"], conf["interval"], conf["at_sec"]    
    print host, port, nclients, interval, at_sec

    print ">>>>>>>>>>>>>connect start:", time.time()
    for i in range(nclients):
        wait = random.random() * 60
        url = "http://%s:%d/frontier_test/?id=%s_%d" % (host, port, util.getip().replace(".", "_"), i)
        timer.Timer().add(wait, http_client.request, (url,))
    print "<<<<<<<<<<<<<connect end:", time.time()

if __name__ == '__main__':
    settings.isClient = True
    ascurl.get("http://127.0.0.1:6000/serviceinfo", start)
    engine.Engine().run()
