import SimpleHTTPServer
import SocketServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from cStringIO import StringIO
import logging

from app.meir.request_handler import RequestHandler


class HttpRequestsHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/xml')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        logging.info("started to handle request")
        # request_handler = RequestHandler("http://meirtv.co.il/site/set.asp?id=22939")
        # lessons_rss = request_handler.get_lessons_rss()

        logging.info("finnished to handle request")
        self.wfile.write(self.get_expected_rss_file())

    def get_expected_rss_file(self):
        with open("../../tests/expected_rss.xml", "r") as myfile:
            data = myfile.read()
        return data
