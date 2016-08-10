import debug
import http_client

callbacks = {}

def register(fd, callback):
    global callbacks
    callbacks[fd] = callback

def on_http_data(fd, http_body):
    callback=callbacks.get(fd)
    if callback != None:
        callback(fd, http_body)
    else:
        http_client.response(fd, http_body)

def on_socket_data(fd, data):
    if not data.endswith("\r\n0\r\n\r\n"):
        return 0
    blocks = data.split("\r\n\r\n")
    body = blocks[1][:]
    idx = body.find("\r\n")
    length = int(body[:idx],16)
    body = body[idx+2:]
    on_http_data(fd, body)
    return len(data)

def on_data(fd, data):
    if debug.Debug:
    	print "--------------->>>>>>data:\n"
    	print data
    	print "------------------------"
    length = on_socket_data(fd, data)
    return length
