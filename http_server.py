import debug
import http_protocol
import engine

def response(url):
    eng = engine.Engine()
    response = http_protocol.responseData("[Keep-Alive Test connections=%d, msgs=%d, qps=%d, max_qps=%d]" % (eng.status.n, eng.status.msgs, eng.status.qps, eng.status.max_qps))
    if debug.Debug:
        print "sendResponse:", response
    return response
