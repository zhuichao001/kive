import util
import json

def getconfig():
    body = util.request("http://10.6.131.78:6001")
    conf = json.loads(body)
    print conf
    ip = conf["ip"] 
    port = conf["port"] 
    clients = conf["clients"]
    interval = conf["interval"]
    at_sec = conf["at_sec"]

    return ip, port, clients, interval, at_sec
