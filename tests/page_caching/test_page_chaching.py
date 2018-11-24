import time
import unittest

from app.meir.html_page_fetching.cache.rss_cache import RSSCache


class MyTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MyTestCase, self).__init__(*args, **kwargs)
        self.google_home_page_url = "www.google.com"
        self.google_home_page_string = self.__get_google_home_page()

    def test_successful_caching(self):
        rss_cache = RSSCache(cache_max_size=1, cache_ttl_seconds=1)

        rss_cache.update_cache(key=self.google_home_page_string,
                               value=self.google_home_page_string)
        cached_value = rss_cache.get_from_cache(key=self.google_home_page_string)
        self.assertEqual(cached_value, self.google_home_page_string)

    def cache_key_overwrite(self):
        rss_cache = RSSCache(cache_max_size=1, cache_ttl_seconds=1)
        rss_cache.update_cache(key=self.google_home_page_string,
                               value=self.google_home_page_string)
        overwrited_value = "world"
        rss_cache.update_cache(key=self.google_home_page_url, value=overwrited_value)
        cached_value = rss_cache.get_from_cache(key=self.google_home_page_string)
        self.assertEqual(cached_value, overwrited_value)

    def test_afer_max_capacity_cache(self):
        rss_cache = RSSCache(cache_max_size=1, cache_ttl_seconds=1)
        rss_cache.update_cache(key=self.google_home_page_string,
                               value=self.google_home_page_string)
        rss_cache.update_cache(key="hello", value="world")
        cached_value = rss_cache.get_from_cache(key=self.google_home_page_string)
        self.assertEqual(cached_value, None)

    def test_after_ttl_cache(self):
        rss_cache = RSSCache(cache_max_size=1, cache_ttl_seconds=1)
        rss_cache.update_cache(key=self.google_home_page_string,
                               value=self.google_home_page_string)
        time.sleep(1.1)
        cached_value = rss_cache.get_from_cache(key=self.google_home_page_string)
        self.assertEqual(cached_value, None)

    def __get_google_home_page(self):
        with open("resources/google_main_page", "r") as myfile:
            data = myfile.read()
        return data

if __name__ == '__main__':
    unittest.main()
