import http.server as BaseHTTPServer

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write('Nothing to see here.'.encode('latin-1'))
        return

    def log_message(self, fmt, *args):
        return
