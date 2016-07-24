#!/usr/bin/python
#-*- coding:utf-8 -*-

import socket
import struct
import fcntl
import time

import sys
import urllib, urllib2

Debug = False

def getip(ethname="eth0"):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', ethname[:15]))[20:24])

def hour_min_sec():
    return time.strftime("%H:%M:%S", time.localtime(time.time()))

def timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

def timeit(func):  
	def wrapper():  
		start = time.clock()  
		func()  
		end =time.clock()  
		print 'used:', end - start  
	return wrapper  

def request(url, postdata=None, repeated=1):
    url =  url if url.startswith("http") else "http://"+url
    for i in range(repeated):
        try:
            if postdata==None or len(postdata)==0:
                return urllib2.urlopen(url).read()
            else:
                if isinstance(postdata, unicode):
                    postdata = postdata.encode('utf-8')
                req = urllib2.Request(url, postdata)
                response = urllib2.urlopen(req)
                return response.read()
        except IOError, e:
            if hasattr(e, 'reason'):
                print 'Failed to reach a server, Reason: ', e.reason
            if hasattr(e, 'read'):
                print 'Error code: ', e.code
        except Exception, e:
            print "Exception:", e
    print >> sys.stderr, "Failed to vist:", url
    return None

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    print timestamp()
    print hour_min_sec()
    print getip('eth0')

    print request("www.baidu.com")
