import unittest
import xml.etree.ElementTree

from app.meir.html_page_fetching.lessons_page_iterator_factory import LessonsPageIteratorFactory
from app.meir.html_page_fetching.web_driver_proxy import WebDriverProxy
from app.meir.html_page_fetching.web_driver_repository import WebDriverRepository
from app.meir.request_handler import RequestHandler
from app.meir.scraping.html_lessons_page_scraper import LessonsPageScraper


class MyTestCase(unittest.TestCase):

    def test_successful_rss_output(self):
        lessons_page_scraper = LessonsPageScraper()
        url_to_scrap = "file:///home/eran/python_tests/meir_app/tests/lesson_test_page"
        web_drivers_repository = WebDriverRepository()
        web_driver_proxy = WebDriverProxy(web_drivers_repository)
        lessons_page_iterator_factory = LessonsPageIteratorFactory(web_driver_proxy)

        request_handler = RequestHandler(url_to_scrap, lessons_page_scraper, lessons_page_iterator_factory)
        expected_rss = self.get_expected_rss_file()
        actual_rss = request_handler.get_lessons_rss()
        self.assertEquals(
            self.remove_last_buid_date_tag(expected_rss),
            self.remove_last_buid_date_tag(actual_rss)
        )

    def get_expected_rss_file(self):
        with open("expected_rss.xml", "r") as myfile:
            data = myfile.read()
        return data

    def remove_last_buid_date_tag(self, data):
        parsed_rss = xml.etree.ElementTree.fromstring(data)
        channel_tag = parsed_rss.find("channel")
        last_buid_date_tag = channel_tag.find("lastBuildDate")
        channel_tag.remove(last_buid_date_tag)
        return xml.etree.ElementTree.tostring(parsed_rss, encoding="UTF-8")

if __name__ == '__main__':
    unittest.main()
