#-*- coding:utf-8 -*-
import socket, select, errno
import sys
import time
import traceback
import kive.event.timer as timer
import kive.http.dispatcher_server as dispatcher_server
import kive.config.settings as settings
import kive.common.util as util
import kive.status.status as status
from kive.common.singleton import *

@singleton
class Engine:
    def __init__(self):
        self.is_server = False
        self.epoll = select.epoll()

        self.fd2con   = {}
        self.incache  = {}
        self.outcache = {}

        #handlers
        self.inHandlers      = {}
        self.onDataHandlers  = {}
        self.onCloseHandlers = {}
        self.onOutHandlers   = {}

        #status
        self.status = status.status
        self.timer = timer.Timer()
        self.timer.add(1, self.updateStatus);

    def updateStatus(self):
        if self.status.update() or time.time()-self.status.last_print>10:
            self.status.Print()
        self.timer.add(1, self.updateStatus);

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

    def connect(self, ip, port, on_connect_handler, on_connect_parameters):
        con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        con.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        con.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        con.setblocking(0)
        err = con.connect_ex((ip, port))
        if err == errno.EINPROGRESS: #ok
            pass
        elif err == errno.EADDRNOTAVAIL: #not available
            return -1
        self.register(con, self.receive, on_connect_handler(*on_connect_parameters))
        return con.fileno()

    def send_delay(self, fd, data, seconds=1):
        self.outcache[fd] += data
        self.timer.add(seconds, self.send_out, (fd, ))

    def send_nodelay(self, fd, data):
        self.outcache[fd] += data
        self.send_out(fd)

    def send_out(self, fd):
        if not self.fd2con.get(fd):
            print >> sys.stderr, "Warning: before send,", fd, "has been closed."
            return -1
        try:
            while len(self.outcache[fd]) > 0:
                written = self.fd2con.get(fd).send(self.outcache[fd])
                self.outcache[fd] = self.outcache[fd][written:]
            if self.onOutHandlers.get(fd):
                self.onOutHandlers[fd]()
            self.epoll.modify(fd, select.EPOLLIN | select.EPOLLET | select.EPOLLHUP | select.EPOLLERR)
            if settings.Debug:
                print util.timestamp(), "send_out over, fd=", fd
        except socket.error, msg:
            if msg.errno == errno.EAGAIN:
                if settings.Debug:
                    print fd, "send again"
                self.epoll.modify(fd, select.EPOLLOUT | select.EPOLLET | select.EPOLLHUP | select.EPOLLERR)
            else:
                print >> sys.stderr, "send faliled, fd=%d, msg=%s" % (fd, msg)
                self.close(fd)
        except Exception, e:
            print >> sys.stderr, "Error:%d send failed: err_msg=%s" % (fd, str(err_msg))
            self.close(fd)

    def run(self):
        while 1:
            self.loop()

    def receive(self, con):
        fd = con.fileno()
        try:
            tmp = con.recv(1024000)
            if tmp:
                if settings.Debug:
                    print fd, "READ:<<<", tmp,">>>"
                self.incache[fd] = self.incache.get(fd, "") + tmp
                return 0
            else: # when the oper side closed
                if settings.isClient:
                    print "EMPTY READ:", fd, tmp
                self.close(fd)
                return -1
        except socket.error, msg:
            if msg.errno == errno.EAGAIN :
                if settings.Debug:
                    print "EAGAIN :", fd
                in_data, out_data = self.onDataHandlers[fd](fd, self.incache[fd])
                self.incache[fd] = in_data
                self.send_nodelay(fd, out_data)
                self.epoll.modify(fd, select.EPOLLET | select.EPOLLHUP | select.EPOLLERR)
                return 1
            elif msg.errno == errno.EWOULDBLOCK:
                if settings.Debug:
                    print fd, "errno.EWOULDBLOCK"
                self.close(fd)
                return -1
            else:
                print >> sys.stderr, "ERROR:fd = %d." % (fd), str(msg)
                self.close(fd)
                return -1

    def loop(self):
        sec = self.timer.watch()    #deal timer and get known of next tick
        events = self.epoll.poll(sec)
        for fd, event in events:
            con = self.fd2con.get(fd)
            try:
                if event & select.EPOLLHUP:
                    print util.timestamp(), "select.EPOLLHUP,fd=", fd
                    if self.onCloseHandlers.get(fd):
                        self.onCloseHandlers[fd]()
                    self.close(fd)
                elif event & select.EPOLLERR:
                    print >> sys.stderr, util.timestamp(), "select.EPOLLERR,fd=", fd
                    if self.onCloseHandlers.get(fd):
                        self.onCloseHandlers[fd]()
                    self.close(fd)
                elif event & select.EPOLLIN:
                    while 1:
                        err = self.inHandlers[fd](con)
                        if err!=0:
                            break
                elif event & select.EPOLLOUT:
                    if settings.Debug:
                        print util.timestamp(),fd,"select.EPOLLOUT"
                    self.send_out(fd)
                else:
                    print("WARNING, UNKNOWN event:", event)
            except:
                traceback.print_exc()

    def close(self, fd):
        try:
            if settings.Debug:
                print "Notation, CLOSE fd=",fd
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
