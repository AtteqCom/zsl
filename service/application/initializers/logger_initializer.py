from application.service_application import service_application
import logging

class LoggerInitializer:
    def initialize(self, app):
        # TODO - Z konfiguracie
        file_handler = logging.FileHandler("/tmp/sportky-service.log")
        file_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(file_handler)


