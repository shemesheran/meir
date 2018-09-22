from BaseHTTPServer import HTTPServer

from app.meir.http_requests_hendler import HttpRequestsHandler

SERVER_PORT = 8080

def start_server(server_class=HTTPServer, handler_class=HttpRequestsHandler, port=SERVER_PORT):
    print "starting server"
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

start_server()
