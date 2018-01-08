#!/usr/bin/python 
#-*- coding:utf-8 -*-

import sys
import socket
import json
import random
import struct
import kive.http.http_server as http_server
import kive.http.http_protocol as http_protocol
import kive.config.settings as settings
from kive.app.app import *
import kive.status.status as status


def on_http_data(fd, http_req):
    if settings.Debug:
        print "body:", http_req
    url = http_req[:http_req.find("\r\n")].split(" ")[1]
    if settings.Debug:
        print fd, url

    status.status.msgs += 1
    status.status.add_remote(fd, url)

    return  "", http_protocol.responseData("hello...")

def on_socket_data(fd, data):
    if not data.endswith("\r\n\r\n"):
        return data, ""
    return on_http_data(fd, data)

def on_data(fd, data):
    return on_socket_data(fd, data)
