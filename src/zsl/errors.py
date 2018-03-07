from abc import ABCMeta, abstractmethod
from typing import List


class ZslError(Exception):
    """
    A base class intended for all exceptions thrown by ZSL or ZSL application.
    """
    pass


ERROR_CONFIG_NAME = 'ERRORS'


class ErrorHandler(object):
    """
    Custom error handler providing a response on a particular error.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def can_handle(self, e):
        """
        Indicator if the handler is able to handle the given exception `e`.

        :param e: The exception that shall be determined if can be handled by the handler.
        :return: `True` or `False` depending on whether the handler can/should handle the method.
        """
        # type: (ErrorHandler, Exception)->bool
        pass

    @abstractmethod
    def handle(self, e):
        """
        Handle the exception.

        :param e: The handled exception.
        :return: The error response for the exception.
        """
        # type: (ErrorHandler, Exception)->bool
        pass


class ErrorProcessor(object):
    """
    Custom error processor handling an error state caused by an error. For example an error processor may only log an
    error, send an email, etc. The main difference between an `ErrorProcessor` and an `ErrorHandler` is that the latter
    one returns a response. There may be only a single `ErrorHandler` returning whereas there may be more
    `ErrorProcessors` handling the same error.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def handle(self, e):
        # type: (ErrorHandler, Exception)->None
        pass


class ErrorConfiguration(object):
    """
    The configuration object for error handling.
    """

    def __init__(self, handlers=None, processors=None, use_flask_handler=False):
        # type: (List[ErrorHandler], List[ErrorProcessor], bool)->None
        self._use_flask_handler = use_flask_handler
        self._handlers = handlers if handlers is not None else []
        self._processors = processors if processors is not None else []

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

    @property
    def processors(self):
        # type: ()->List[ErrorProcessor]
        return self._processors
