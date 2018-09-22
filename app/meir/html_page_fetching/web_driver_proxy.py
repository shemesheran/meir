class WebDriverProxy:
    def __init__(self, web_driver_repository):
        self.web_driver_repository = web_driver_repository

    def execute_with_web_driver(self, function):
        web_driver = self.web_driver_repository.get_web_driver()
        return_val = function(web_driver)
        self.web_driver_repository.return_web_driver(web_driver)
        return return_val

