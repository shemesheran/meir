# -*- coding: utf-8 -*-

import unittest
from app.meir.scraping.html_lessons_page_scraper import LessonsPageScraper

class ScraperTest(unittest.TestCase):
    def test_successful_lessons_scraping(self):
        test_file = open("resources/lesson_test_page")
        scraper = LessonsPageScraper()
        lessons = scraper.scrap_lessons(test_file)
        first_lesson = lessons[0]
        self.assertEquals(first_lesson.code, 68660)
        self.assertEquals(first_lesson.audio_url, "http://mp3.meirtv.co.il/Sherki/095/Idx 68660.mp3")

    def test_failing_lesssons_scraping(self):
        test_file = open("resources/google_main_page")
        scraper = LessonsPageScraper()
        lessons_list = scraper.scrap_lessons(test_file)
        self.assertEqual(len(lessons_list), 0)

    def test_successful_get_title(self):
        test_file = open("resources/lesson_test_page")
        scraper = LessonsPageScraper()
        expected_text = u"""שם הסדרה: הספרייה של היהדות   מבוא לתורה שבעל פה
מחזור: התשעח
שם הרב: הרב אורי עמוס שרקי """
        returned_text = scraper.scrap_lessons_series_title(test_file)
        self.assertEquals(expected_text, returned_text)

    def test_failing_get_title(self):
        test_file = open("resources/google_main_page")
        scraper = LessonsPageScraper()
        self.assertRaises(Exception, scraper.scrap_lessons_series_title, test_file)

if __name__ == '__main__':
    unittest.main()
