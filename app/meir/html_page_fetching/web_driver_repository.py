from Queue import Queue
from selenium import webdriver

from selenium.webdriver.chrome.options import Options

class WebDriverRepository:

    __number_of_web_drivers_in_queue = 1
    __get_web_driver_timeout_seconds = 5
    __executable_path = "/home/eran/Documents/chromedriver"

    def __init__(self):
        self.__web_drivers_queue = Queue()
        self.__populate_web_drivers_queue()

    def __populate_web_drivers_queue(self):
        for i in range(self.__number_of_web_drivers_in_queue):
            web_driver = self.__init_web_driver()
            self.__web_drivers_queue.put_nowait(web_driver)

    def __init_web_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        return webdriver.Chrome(chrome_options=chrome_options,
                                executable_path=self.__executable_path)


    def get_web_driver(self):
        return self.__web_drivers_queue.get(timeout=self.__get_web_driver_timeout_seconds)

    def return_web_driver(self, web_driver):
        self.__web_drivers_queue.put_nowait(web_driver)

    def __del__(self):
        web_driver = self.get_web_driver()
        while (web_driver is not None):
            web_driver.close()
            web_driver = self.get_web_driver()
