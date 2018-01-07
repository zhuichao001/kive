import time
import util

class Status:
    def __init__(self):
        self.n = 0
        self.msgs = 0
        self.qps = 0
        self.max_qps = 0
        self.last_n = 0
        self.last_msgs = 0
        self.last_time = 0

        self.remotes = {}
        self.remotes_n = 0
        self.last_remotes_n = 0

        self.last_print = 0

    def get_remotes(self):
        return sum([n for n in self.remotes.values()])

    def add_remote(self, fd, id):
        self.remotes[fd] = self.remotes.get(fd, 0) + 1

    def del_remote(self, fd):
        if self.remotes.get(fd):
            del self.remotes[fd]

    def clear_remote(self, con):
        self.remotes[con.fileno()].clear()

    def close(self, fd):
        self.n -= 1
        #self.del_remote(fd)

    def update(self):
        if self.msgs == self.last_msgs and self.n == self.last_n and self.last_remotes_n == self.remotes_n:
            return False

        now = time.time()
        self.qps = int(float(self.msgs - self.last_msgs) / float(now - self.last_time))
        if self.qps > self.max_qps:
           self.max_qps = self.qps

        self.remotes_n = self.get_remotes()
        self.last_n = self.n
        self.last_msgs = self.msgs
        self.last_time = now
        self.last_remotes_n = self.remotes_n
        return True

    def Print(self):
        print util.hour_min_sec(), "[Status: remotes=%d, connections=%d, msgs=%d, qps=%d, max_qps=%d]" % (self.get_remotes(), self.n, self.msgs, self.qps, self.max_qps)
        self.last_print = time.time()

