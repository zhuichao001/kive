import httpreq
import json

def getconfig():
    body = httpreq.request("http://10.4.43.155:6001")
    conf = json.loads(body)
    print conf
    ip = conf["ip"] 
    port = conf["port"] 
    clients = conf["clients"]
    interval = conf["interval"]

    return ip, port, clients, interval
