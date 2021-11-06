import threading
import http.server as BaseHTTPServer
import socketserver as SocketServer

class ThreadedServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    def __init__(self, *args,**kwargs):
        self.cache = {}
        self.cache_lock = threading.Lock()
        self.args = ""
        self.screen_lock = threading.Lock()
        self.alexa = ""
        self.cisco = ""
        self.exitthread = threading.Event()
        self.exitthread.clear()
        BaseHTTPServer.HTTPServer.__init__(self, *args, **kwargs)

    def safe_print(self, *args, **kwargs):
        try:
            self.screen_lock.acquire()
            print(*args, **kwargs)
        finally:
            self.screen_lock.release()
