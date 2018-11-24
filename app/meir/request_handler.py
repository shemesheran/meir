from app.meir.podcast_rss_generator import MeirPodcastRSSGenerator
import logging

class RequestHandler:

    def __init__(self, request_url, lessons_scraper, lessons_page_iterator_factory, rss_cache):
        self.request_url = request_url
        self.lessons_set = set()
        self.lessons_page_iterator = lessons_page_iterator_factory.get_object(request_url)
        self.lessons_scraper = lessons_scraper
        self.rss_cache = rss_cache

    def get_lessons_rss(self):
        logging.info("Getting lessons RSS for {}".format(self.request_url))
        result_from_cache = self.rss_cache.get_from_cache(self.request_url)
        if(result_from_cache is not None):
            return result_from_cache
        else:
            rss_from_url = self.__try_get_lessons_rss_from_url()
            self.rss_cache.update_cache(self.request_url, rss_from_url)
            return rss_from_url

    def __try_get_lessons_rss_from_url(self):
        try:
            lessons_rss = self.__get_lessons_rss_from_url()
            return lessons_rss
        except Exception, e:
            logging.error("Could not generate RSS for url: {}\n{}".format(self.request_url, e.message))

    def __get_lessons_rss_from_url(self):
        lessons_series_title = self.__get_lessons_series_title()
        lessons_set = self.__get_lessons_set()
        meir_podcast_generator = MeirPodcastRSSGenerator(lessons_series_title, self.request_url)
        podcast_rss = meir_podcast_generator.generate_lessons_podcast_rss(lessons_set)
        return podcast_rss

    def __get_lessons_series_title(self):
        first_page = self.lessons_page_iterator.get_first_page()
        series_title = self.lessons_scraper.scrap_lessons_series_title(first_page)
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
