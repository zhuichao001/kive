import util
import json

def getconfig():
    body = util.request("http://10.6.131.78:6001")
    conf = json.loads(body)
    print conf
    return conf["ip"], conf["port"], conf["clients"], conf["interval"], conf["at_sec"]
