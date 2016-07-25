#!/usr/bin/python 
#-*- coding:utf-8 -*-

import sys
import socket
import json
import random
import engine
import gvar


if __name__ == '__main__':
    gvar.Client = False
    gvar.SetEngine(engine.engine())
    gvar.Engine().bind(port=6000)
    gvar.Engine().run()
