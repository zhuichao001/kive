#!/usr/bin/python 
#-*- coding:utf-8 -*-

import sys
import socket
import json
import random
import struct
import hub
import engine
import gvar

gvar.Client = False

if __name__ == '__main__':
    gvar.SetEngine(engine.engine())
    gvar.Engine().bind(port=6000)
    gvar.Engine().run()
