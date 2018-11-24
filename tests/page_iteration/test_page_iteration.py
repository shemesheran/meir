# -*- coding: utf-8 -*-

import unittest
import os
import codecs
from app.meir.html_page_fetching.lessons_page_iterator_factory import LessonsPageIteratorFactory
from app.meir.html_page_fetching.web_driver_proxy import WebDriverProxy
from app.meir.html_page_fetching.web_driver_repository import WebDriverRepository
from app.meir.scraping.html_lessons_page_scraper import LessonsPageScraper

class MyTestCase(unittest.TestCase):

    base_url = "resources/lesson_test_page"
    scraper = LessonsPageScraper()

    def test_successful_page_iteration(self):
        page_iterator = self.__prepare_iterator()
        self.__test_first_page(page_iterator)
        self.__test_second_page(page_iterator)

    def __test_first_page(self, page_iterator):
        actual_first_page = page_iterator.get_first_page()
        self.assert_page_title_equals(actual_first_page)

    def assert_page_title_equals(self, actual_first_page):
        page_title = self.scraper.scrap_lessons_series_title(actual_first_page)
        expected_page_title = u'''שם הסדרה: הספרייה של היהדות   מבוא לתורה שבעל פה
מחזור: התשעח
שם הרב: הרב אורי עמוס שרקי '''
        self.assertEqual(page_title, expected_page_title)

    def __test_second_page(self, page_iterator):
        actual_second_page = page_iterator.get_next_page()
        self.assert_page_title_equals(actual_second_page)

    def __prepare_iterator(self):
        web_driver_repository = WebDriverRepository(web_drivers_number=1)
        web_driver_proxy = WebDriverProxy(web_driver_repository)
        page_iterator_factory = LessonsPageIteratorFactory(web_driver_proxy)
        local_page_url = self.__get_local_page_url()
        page_iterator = page_iterator_factory.get_object(local_page_url)
        return page_iterator

    def __get_local_page_url(self):
        file_absolute_path = os.path.abspath(self.base_url)
        file_url = "file://{}".format(file_absolute_path)
        return file_url

    def __get_local_page(self, local_test_page_relative_path):
        with codecs.open(local_test_page_relative_path, encoding="UTF-8") as myfile:
            data = myfile.read()
        return data

    def __scrap_lesson_title(self, lesson_row):
        lesson_title = lesson_row.select_one(".titleArchive").text
        return lesson_title


if __name__ == '__main__':
    unittest.main()
