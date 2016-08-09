import gvar
import http_protocol

def response(url):
    e = gvar.Engine()
    response = http_protocol.responseData("[Keep-Alive Test connections=%d, msgs=%d, qps=%d, max_qps=%d]" % (e.status.n, e.status.msgs, e.status.qps, e.status.max_qps))
    if gvar.Debug:
        print "sendResponse:", response
    return response
