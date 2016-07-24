
def get(uri, callback):
    req = req_headers(url = uri[uri.find("/")+1:], host=uri[:uri.find("/")])
    fd = gvar.Engine().connect(gvar.host, gvar.port)
    gvar.Engine().send_nodelay(fd, http_protocol.req_data(fd))

