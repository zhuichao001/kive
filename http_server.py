import settings
import http_protocol
import engine
from app import *

@app.route("/frontier_test/\?id=<remoteid>")
def response_frontier_test(remoteid):
    eng = engine.Engine()
    if settings.Debug:
        print "remoteid:", remoteid
    response = http_protocol.responseData("[Keep-Alive Test connections=%d, msgs=%d, qps=%d, max_qps=%d]" % (eng.status.n, eng.status.msgs, eng.status.qps, eng.status.max_qps))
    if settings.Debug:
        print "sendResponse:", response
    return response
