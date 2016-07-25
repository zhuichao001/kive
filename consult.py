#!/usr/bin/python 
#-*- coding:utf-8 -*-

import sys
import socket
import json
import random
import struct
import gvar

def init()
    e = gvar.Engine()
    e.bind(port=6001)
