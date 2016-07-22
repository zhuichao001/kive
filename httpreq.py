#!/usr/bin/python 
#-*- coding:utf-8 -*-

import urllib
import urllib2
import sys
import time

Debug = False

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

if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print request("www.baidu.com")
