
import time
import json
from kive.app.app import *
import kive.http.http_protocol as http_protocol

conf_info = {
    "ip": "120.77.13.45",
    "port": 6000, 
    "clients": 400,
    "interval": 60,
    "at_sec": int(time.time())+10
}

@app.route("/serviceinfo")
def service_info():
    response = http_protocol.responseData(json.dumps(conf_info))
    return response

if __name__ == '__main__':
    print app.serve("/serviceinfo")
