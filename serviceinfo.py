
import time
from app import *
import json
import http_protocol

conf_info = {
    "ip": "10.6.131.78",
    "port": 6000, 
    "clients": 400,
    "interval": 60,
    "at_sec": int(time.time())+10
}

@app.route("/serviceinfo")
def service_info():
    response = http_protocol.responseData(json.dumps(conf_info))
    return response

"""
if __name__ == '__main__':
    print app.serve("/serviceinfo")
"""
