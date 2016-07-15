#!/usr/bin/python 
#-*- coding:utf-8 -*-

import urllib
import urllib2
import sys
import time

Debug = False

def request(url, postdata=None, repeated=1):
    suc = False
    file = ""
    if isinstance(postdata,unicode):
        postdata = postdata.encode('utf-8')

    url =  url if url.startswith("http://") else "http://"+url

    for i in range(0,repeated):
        try:
            start = time.time()
            if postdata==None or len(postdata)==0:
                file = urllib2.urlopen(url).read()
            else:
                req = urllib2.Request(url, postdata)
                response = urllib2.urlopen(req)
                file = response.read()
            end = time.time()

            m = "POST" if postdata else "GET"
            if Debug:
                print "URL:", url, "METHOD:", m, "COST:", end-start
            suc = True
            break
        except IOError, e:
            if hasattr(e, 'reason'):
                if i==0:
                    print 'We failed to reach a server.','Reason: ', e.reason
            if hasattr(e, 'read'):
                if i==0:
                    print 'Error code: ', e.code
                file = e.read()
        except Exception,e:
            print "Exception,",e
            print e

    if not suc:
        print "Failed to vist:", url
    return file

if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print content
