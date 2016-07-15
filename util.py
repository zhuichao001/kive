#!/usr/bin/python

import socket
import struct
import fcntl

import time

def getip(ethname="eth0"):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', ethname[:15]))[20:24])

def hour_min_sec():
    return time.strftime("%H:%M:%S", time.localtime(time.time()))

def timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

if __name__ == '__main__':
    print timestamp()
    print hour_min_sec()
    print getip('eth0')
