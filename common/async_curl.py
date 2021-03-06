import kive.event.engine as engine
import kive.http.http_client as http_client
import hkive.http.ttp_client as ttp_client


def get(uri, callback):
    def on_response(fd, data):
        print "RECEIVED(GET):", data
        callback(data)
    req = http_client.request(url=uri, callback=on_response)

def post(uri, data, callback):
    def on_response(fd, data):
        print "RECEIVED(POST):", data
        callback(data)
    req = http_client.request(url=uri, post=data, callback=on_response)

def on_data(data):
    print data

if __name__ == '__main__':
    get("http://127.0.0.1:6001/", on_response)
    engine.Engine().run()
