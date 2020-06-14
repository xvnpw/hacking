from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import urllib.parse
import sys
import logging

logger = logging.getLogger('server')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('server.log')
logger.addHandler(fh)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path=urllib.parse.unquote(self.path)
        print("path", path)
        logger.info("headers: %s", self.headers)
        if path.startswith('/?r',0,3):
                to_url=path[4:]
                print("to_url",to_url)
                self.send_response(302)
                self.send_header('Location', to_url)
                self.end_headers()
        else:
                file_to_read=path[1:]
                print("file_to_read", file_to_read)
                self.send_response(200)
                self.send_header("Content-type", "image/svg+xml")
                self.end_headers()
                file=open(file_to_read,"rb")
                self.wfile.write(file.read())


PORT=int(sys.argv[1])
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    logger.info("serving at port %s",PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
