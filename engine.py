#-*- coding:utf-8 -*-
import socket, select, errno
import os,sys
import time
import heapq
import signal
import dispatcher_client
import dispatcher_server
import gvar
import util
import random
import traceback
from singleton import *

class Engine:
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

    def __init__(self):
        self.is_server = False
        self.epoll = select.epoll()

        self.fd2con   = {}
        self.incache  = {}
        self.outcache = {} #outcache for send

        #handlers
        self.inHandlers      = {}
        self.onDataHandlers  = {}
        self.onCloseHandlers = {}
        self.onOutHandlers   = {}

        #status
        self.status = Engine.Status()
        gvar.Timer().add(1, self.updateStatus);


    def updateStatus(self):
        if self.status.update() or time.time()-self.status.last_print>10:
            self.status.Print()
        gvar.Timer().add(1, self.updateStatus);
    #def addcycle(self, cycle, callback, args=()); #TODO

    def register(self, con, in_handler, data_handler, out_handler=None, close_handler=None):
        fd = con.fileno()
        con.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,4096) 
        con.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,4096) 

        self.fd2con[fd]           =  con
        self.incache[fd]          =  ""
        self.outcache[fd]         =  ""
        self.inHandlers[fd]       =  in_handler
        self.onDataHandlers[fd]   =  data_handler
        self.onCloseHandlers[fd]  =  close_handler
        self.onOutHandlers[fd]    =  out_handler

        self.status.n += 1
        self.epoll.register(fd, select.EPOLLIN | select.EPOLLET | select.EPOLLHUP | select.EPOLLERR)

    def unregister(self, fd):
        self.status.close(fd)
        del self.fd2con[fd]
        del self.incache[fd]
        del self.outcache[fd]
        del self.onDataHandlers[fd]
        del self.onCloseHandlers[fd]
        del self.onOutHandlers[fd]

    def bind(self, port):
        self.is_server = True
        svrsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        svrsocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        svrsocket.bind(("0.0.0.0", port))
        self.register(svrsocket, self.accept, None)
        svrsocket.listen(1024768)
        svrsocket.setblocking(0)
        return svrsocket

    def accept(self, svr_con):
        try:
            con, address = svr_con.accept()
            con.setblocking(0)
            self.register(con, self.receive, dispatcher_server.on_data)
            return 0
        except socket.error, msg:
            if msg.errno != errno.EAGAIN:
                traceback.print_exc()
            return -1

    def connect(self, ip, port):
        con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        con.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        con.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        con.setblocking(0)
        err = con.connect_ex((ip, port))
        if err == errno.EINPROGRESS: #ok
            pass
        elif err == errno.EADDRNOTAVAIL: #not available
            return -1
        self.register(con, self.receive, dispatcher_client.on_data)
        return con.fileno()

    def send_delay(self, fd, data, seconds=1):
        self.outcache[fd] += data
        gvar.Timer().add(seconds, self.send_out, (fd, ))

    def send_nodelay(self, fd, data):
        self.outcache[fd] += data
        self.send_out(fd)

    def send_out(self, fd):
        if not self.fd2con.get(fd):
            print "Warning: before send,", fd, "has been closed."
            return -1
        try:
            if gvar.Debug:
                print util.timestamp(), "to send_out", fd
            while len(self.outcache[fd]) > 0:
                written = self.fd2con.get(fd).send(self.outcache[fd])
                if gvar.Debug:
                    print "send_out written:", written
                self.outcache[fd] = self.outcache[fd][written:]
            if self.onOutHandlers.get(fd):
                self.onOutHandlers[fd]()
            self.epoll.modify(fd, select.EPOLLIN | select.EPOLLET | select.EPOLLHUP | select.EPOLLERR)
            if gvar.Debug:
                print util.timestamp(), "send_out!!!!!!!", fd
        except socket.error, msg:
            if msg.errno == errno.EAGAIN:
                if gvar.Debug:
                    print fd, "send again"
                self.epoll.modify(fd, select.EPOLLOUT | select.EPOLLET | select.EPOLLHUP | select.EPOLLERR)
            else:
                print fd, "send faliled", msg
                self.closeClient(fd)
        except Exception, e:
            print("Error:%d send failed: err_msg=%s" % (fd, str(err_msg)) )
            self.closeClient(fd)

    def run(self):
        while 1:
            self.lookup()


    def receive(self, con):
        fd = con.fileno()
        try:
            tmp = con.recv(1024000)
            if tmp: #and not self.incache.get(fd):
                if gvar.Debug:
                    print "READ:", fd, tmp
                self.incache[fd] = self.incache.get(fd,"") + tmp
                return 0
            else: # the oper side closed
                if gvar.Client:
                    print "EMPTY READ:", fd, tmp
                self.closeClient(fd)
                return -1
        except socket.error, msg:
            if msg.errno == errno.EAGAIN :
                if gvar.Debug:
                    print "EAGAIN READ:", fd
                n = self.onDataHandlers[fd](fd, self.incache[fd])
                self.incache[fd] = self.incache[fd][n:]
                self.epoll.modify(fd, select.EPOLLET | select.EPOLLHUP | select.EPOLLERR)
                return 1
            elif msg.errno == errno.EWOULDBLOCK:
                print fd, "errno.EWOULDBLOCK"
                self.closeClient(fd)
                return -1
            else:
                print "error:fd = %d." % (fd), str(msg)
                self.closeClient(fd)
                return -1

    def lookup(self):
        sec = gvar.Timer().watch()    #deal timer and get known of next tick
        events = self.epoll.poll(sec)
        for fd, event in events:
            con = self.fd2con.get(fd)
            try:
                if event & select.EPOLLHUP:
                    print util.timestamp(),"!!!!!!select.EPOLLHUP,fileno=",fd 
                    if self.onCloseHandlers.get(fd):
                        self.onCloseHandlers[fd]()
                    self.closeClient(fd)
                elif event & select.EPOLLERR:
                    print("!!!!!!select.EPOLLERR,fileno=", fd)
                    if self.onCloseHandlers.get(fd):
                        self.onCloseHandlers[fd]()
                    self.closeClient(fd)
                elif event & select.EPOLLIN:
                    if gvar.Debug:
                        print "select.EPOLLIN"
                    while 1:
                        err = self.inHandlers[fd](con)
                        if err!=0:
                            break
                elif event & select.EPOLLOUT:
                    print util.timestamp(),fd,"select.EPOLLOUT"
                    self.send_out(fd)
                else:
                    print("!!!unknown event:", event)
            except:
                traceback.print_exc()

    def closeClient(self, fd):
        try:
            if gvar.Debug:
                print "closeClient fd=",fd
            self.unregister(fd)
            self.epoll.unregister(fd)
            if fd in self.fd2con:
                self.fd2con[fd].shutdown(socket.SHUT_RDWR)
                self.fd2con[fd].close()
        except Exception,e:
            traceback.print_exc()

if __name__ == '__main__':
    e=Engine()
    e.run()
