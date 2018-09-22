from app.meir.html_page_fetching.lessons_page_iterator import LessonsPageIterator
from app.meir.scraping.html_lessons_page_scraper import LessonsPageScraper
from app.meir.podcast_rss_generator import MeirPodcastRSSGenerator


class RequestHandler:

    def __init__(self, request_url, lessons_scraper, lessons_page_iterator_factory):
        self.request_url = request_url
        self.lessons_set = set()
        self.lessons_page_iterator = lessons_page_iterator_factory.get_object(request_url)
        self.lessons_scraper = lessons_scraper

    def get_lessons_rss(self):
        lessons_series_title = self.__get_lessons_series_title()
        lessons_set = self.__get_lessons_set()
        meir_podcast_generator = MeirPodcastRSSGenerator(lessons_series_title, self.request_url)
        podcast_rss = meir_podcast_generator.generate_lessons_podcast_rss(lessons_set)
        return podcast_rss

    def __get_lessons_series_title(self):
        first_page = self.lessons_page_iterator.get_first_page()
        series_title = self.lessons_scraper.get_lessons_series_title(first_page)
        return series_title

    def __get_lessons_set(self):
        while (True):
            current_lessons_set = self.__get_next_lessons_set()
            if (self.__is_new_lessons(current_lessons_set)):
                self.lessons_set.update(current_lessons_set)
            else:
                break
        return self.lessons_set

    def __get_next_lessons_set(self):
        current_lessons_page = self.lessons_page_iterator.get_next_page()
        current_lessons = self.lessons_scraper.scrap_lessons(current_lessons_page)
        current_lessons_set = set(current_lessons)
        return current_lessons_set

    def __is_new_lessons(self, lessons):
        return not self.lessons_set.issuperset(lessons)
