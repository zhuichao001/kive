
import kive.config.settings as settings
import kive.http.http_protocol as http_protocol
import kive.status.status as status
from kive.app.app import *

@app.route("/hello_test/\?id=<remoteid>")
def response_frontier_test(remoteid):
    if settings.Debug:
        print "remoteid:", remoteid
    response = http_protocol.responseData("[Keep-Alive Test connections=%d, msgs=%d, qps=%d, max_qps=%d]" % (status.status.n, status.status.msgs, status.status.qps, status.status.max_qps))
    if settings.Debug:
        print "sendResponse:", response
    return response
