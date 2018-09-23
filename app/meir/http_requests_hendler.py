import SimpleHTTPServer
import SocketServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from cStringIO import StringIO
import logging

from app.meir.html_page_fetching.lessons_page_iterator import LessonsPageIterator
from app.meir.html_page_fetching.lessons_page_iterator_factory import LessonsPageIteratorFactory
from app.meir.html_page_fetching.web_driver_proxy import WebDriverProxy
from app.meir.html_page_fetching.web_driver_repository import WebDriverRepository
from app.meir.request_handler import RequestHandler
from app.meir.scraping.html_lessons_page_scraper import LessonsPageScraper


class HttpRequestsHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    lessons_page_scraper = LessonsPageScraper()
    web_drivers_repository = WebDriverRepository()
    web_driver_proxy = WebDriverProxy(web_drivers_repository)
    lessons_page_iterator_factory = LessonsPageIteratorFactory(web_driver_proxy)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/xml')
        self.end_headers()

    def do_GET(self):
        logging.info("handling a GET request")
        self._set_headers()
        request_handler = RequestHandler("http://meirtv.co.il/site/set.asp?id=22939",
                                         self.lessons_page_scraper,
                                         self.lessons_page_iterator_factory)
        lessons_rss = request_handler.get_lessons_rss()

        logging.info("finished to handle GET request")
        self.wfile.write(lessons_rss)
