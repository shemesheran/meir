from app.meir.html_page_fetching.lessons_page_iterator import LessonsPageIterator

class LessonsPageIteratorFactory():
    def __init__(self, web_driver_proxy):
        self.web_driver_proxy = web_driver_proxy

    def get_object(self, starting_url):
        return LessonsPageIterator(starting_url=starting_url,
                                   web_driver_proxy=self.web_driver_proxy)