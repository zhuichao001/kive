import engine
import http_client
import http_client


def get(uri, callback):
    def on_response(fd, data):
        print "RECEIVED:", data
        callback(data)
    req = http_client.request(url=uri, callback=on_response)

def on_data(data):
    print data

if __name__ == '__main__':
    get("http://127.0.0.1:6001/", on_response)
    engine.Engine().run()
