import heapq
import time
from singleton import *

@singleton
class Timer:
    def __init__(self):
        self.timers = []

    def add(self, after_sec, callback, args=()):
        heapq.heappush(self.timers, (time.time()+after_sec, callback, args))

    def at(self, at_sec, callback, args=()):
        heapq.heappush(self.timers, (at_sec, callback, args))

    def remove(self, ):
        pass #TODO

    def watch(self):
        now = time.time()
        while self.timers:
            sec, callback, args = heapq.heappop(self.timers)
            if sec<now:
                callback(*args)
            else:
                heapq.heappush(self.timers, (sec, callback, args))
                return 0.001 if (sec-now)<0.001 else (sec-now)

if __name__ == '__main__':
    def ok():
        print "ok"
    t = Timer()
    t.add(2, ok)
    while True:
        t.watch()
