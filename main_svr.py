#!/usr/bin/python 
#-*- coding:utf-8 -*-

import sys
import socket
import json
import random
import engine
import debug


if __name__ == '__main__':
    debug.isClient = False
    eng = engine.Engine()
    eng.bind(port=6000)
    eng.run()
