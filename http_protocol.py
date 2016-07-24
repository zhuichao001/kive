import util
import gvar

def req_data(fd):
    url = "/frontier_test/?id=%s_%d" % (util.getip().replace(".", "_"), fd)
    return req_headers(url, gvar.host)

def req_headers(url, host, is_gzip=False):
    gzip_param = "Accept-Encoding: gzip, deflate, sdch\r\n"
    if is_gzip == False:
        gzip_param = ""
    headers = \
"GET %s HTTP/1.1\r\n\
Accept: application/text; version=1.0\r\n\
Accept-Language: zh-CN,zh\r\n\
Host: %s\r\n\
%s\
Connection: Keep-Alive\r\n\r\n" % (url, host, gzip_param)
    return headers

def responseData(content):
    headers = \
"""HTTP/1.1 200 OK\r\n\
Context-Type: text/plain; charset=utf-8\r\n\
Content-Length: %d\r\n\
Connection: Keep-Alive\r\n\r\n\
%s\r\n\
%s\r\n\r\n\
0\r\n\r\n\
""" % (len(content), hex(1+len(content))[2:], content)
    return headers

