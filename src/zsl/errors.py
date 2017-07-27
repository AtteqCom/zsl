from abc import ABCMeta, abstractmethod
from typing import List


class ZslError(Exception):
    pass


ERROR_CONFIG_NAME = 'ERRORS'


class ErrorHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def can_handle(self, e):
        pass

    @abstractmethod
    def handle(self, e):
        pass


class ErrorConfiguration(object):
    def __init__(self, handlers=None, use_flask_handler=False):
        # type: (List[ErrorHandler], bool)->None
        self._use_flask_handler = use_flask_handler
        self._handlers = handlers if handlers is not None else []

    @property
    def use_flask_handler(self):
        # type:()->bool
        """
        In case of web requests, flasks provides a convenient way of exception
        handling. This handler shows the stack trace, etc. On the other hand \
        this setting will turn of ZSL's exception handling for web request.

        :return: Status
        """
        return self._use_flask_handler

    @property
    def handlers(self):
        # type: ()->List[ErrorHandler]
        return self._handlers
