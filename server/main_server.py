#!/usr/bin/python 
#-*- coding:utf-8 -*-

import sys
import kive.event.engine as engine
import kive.config.settings as settings


if __name__ == '__main__':
    settings.isClient = False
    eng = engine.Engine()
    eng.bind(port=6000)
    print >>sys.stdout, "LISTEN ON 6000"
    eng.run()
