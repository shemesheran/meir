from urllib import urlencode
from urlparse import urlparse, parse_qs, urlunparse
import logging

class LessonsPageIterator:

    __page_number_parameter_name = 'page'

    def __init__(self, starting_url, web_driver_proxy):
        self.base_url = starting_url
        self.__remove_page_number_parameter_from_url()
        self.page_number = 0
        self.web_driver_proxy = web_driver_proxy

    def get_first_page(self):
        def do_get_first_page(web_driver):
            first_page_url = self.__get_url_with_page_number(1)
            logging.debug("first_page_url: {}".format(first_page_url))
            web_driver.get(first_page_url)
            first_page_source = web_driver.page_source
            return first_page_source

        return self.web_driver_proxy.execute_with_web_driver(do_get_first_page)

    def get_next_page(self):
        def do_get_next_page(web_driver):
            self.__navigate_to_next_page(web_driver)
            next_page = web_driver.page_source
            return next_page

        return self.web_driver_proxy.execute_with_web_driver(do_get_next_page)


    def __navigate_to_next_page(self, web_driver):
        self.page_number = self.page_number + 1
        next_page_url = self.__get_url_with_page_number(self.page_number)
        web_driver.get(next_page_url)

    def __remove_page_number_parameter_from_url(self):
        parsed_url = urlparse(self.base_url)
        get_parameters = parse_qs(parsed_url.query)
        get_parameters.pop(self.__page_number_parameter_name, None)
        parsed_url = parsed_url._replace(query=urlencode(get_parameters, True))
        self.base_url = urlunparse(parsed_url)

    def __get_url_with_page_number(self, page_number):
        parsed_url = urlparse(self.base_url)
        get_parameters = parse_qs(parsed_url.query)
        get_parameters.update({self.__page_number_parameter_name: page_number})
        parsed_url = parsed_url._replace(query=urlencode(get_parameters, True))
        url_with_page_number = urlunparse(parsed_url)
        return url_with_page_number
