import logging

from abc import ABC, abstractmethod

class AbstractHandler(logging.Handler, ABC):

    @abstractmethod
    def emit(self, record):
        pass

class Logger:

    def __init__(self):
        self._logger = logging.getLogger('chat_app')
        self._logger.setLevel(level="INFO")

    def add_handler(self, handler: AbstractHandler):
        if handler not in self._logger.handlers:
            self._logger.addHandler(handler)