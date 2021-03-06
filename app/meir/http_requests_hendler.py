import SimpleHTTPServer
import logging
from urlparse import parse_qs

from app.meir.html_page_fetching.cache.rss_cache import RSSCache
from app.meir.html_page_fetching.lessons_page_iterator_factory import LessonsPageIteratorFactory
from app.meir.html_page_fetching.web_driver_proxy import WebDriverProxy
from app.meir.html_page_fetching.web_driver_repository import WebDriverRepository
from app.meir.request_handler import RequestHandler
from app.meir.scraping.html_lessons_page_scraper import LessonsPageScraper
import ConfigParser

class HttpRequestsHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    config_parser = ConfigParser.ConfigParser()
    config_parser.read("application.conf")
    web_drivers_number = config_parser.get(section="web_drivers", option="number")
    lessons_page_scraper = LessonsPageScraper()
    web_drivers_repository = WebDriverRepository(web_drivers_number)
    web_driver_proxy = WebDriverProxy(web_drivers_repository)
    lessons_page_iterator_factory = LessonsPageIteratorFactory(web_driver_proxy)
    rss_cache = RSSCache(cache_max_size=100, cache_ttl_seconds=3600)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/xml')
        self.end_headers()

    def do_GET(self):
        logging.info("handling a GET request")
        lessons_page_url = self.__get_lessons_page_url()
        self._set_headers()
        request_handler = RequestHandler(lessons_page_url,
                                         self.lessons_page_scraper,
                                         self.lessons_page_iterator_factory,
                                         self.rss_cache)
        lessons_rss = request_handler.get_lessons_rss()

        logging.info("finished to handle GET request")
        self.wfile.write(lessons_rss)

    def __get_lessons_page_url(self):
        parameters = self.__parse_request_parameters()
        lessons_page = parameters["lessons_page"].pop()
        return lessons_page

    def __parse_request_parameters(self):
        return parse_qs(self.path[2:])
