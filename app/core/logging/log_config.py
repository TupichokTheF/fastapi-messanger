import json
import logging, logging.config

from abc import ABC, abstractmethod

from app.core.settings import settings

class AbstractHandler(logging.Handler, ABC):

    @abstractmethod
    def emit(self, record):
        pass

class Logger:
    PATH_TO_CONFIG: str = settings.LOGGING_CONFIG

    def __init__(self):
        self._setup_logging()
        self._logger = logging.getLogger('chat_app')

    def _setup_logging(self):
        with open(self.PATH_TO_CONFIG, 'r') as config_file:
            config = json.load(config_file)
        logging.config.dictConfig(config)

    def add_handler(self, handler: AbstractHandler):
        if handler not in self._logger.handlers:
            self._logger.addHandler(handler)

    def get_logger(self):
        return self._logger

