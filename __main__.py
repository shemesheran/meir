from BaseHTTPServer import HTTPServer

from app.meir.http_requests_hendler import HttpRequestsHandler
import logging
import ConfigParser
from logging.config import fileConfig

SERVER_PORT = 8080

def start_server(server_class=HTTPServer, handler_class=HttpRequestsHandler, port=SERVER_PORT):
    fileConfig('logging_config.ini')
    logging.info("Started web server")
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

start_server()
