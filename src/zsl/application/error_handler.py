"""
:mod:`zsl.application.error_handler`
---------------------------------------------------

This module does the error handling. It allows users to register
an error handler for a given exception type. It also provides default
error handlers.
"""
from __future__ import unicode_literals
from builtins import *

import http.client
import logging
import traceback

from abc import abstractmethod
from flask import request
from functools import wraps

from zsl.db.model.app_model import AppModel
from zsl.router.task import RoutingError
from zsl.task.job_context import add_responder, StatusCodeResponder

from zsl.utils.documentation import documentation_link

_error_handlers = []


class ErrorResponse(AppModel):
    def __init__(self, code, message):
        super(ErrorResponse, self).__init__({})
        self.code = code
        self.message = message


class ErrorHandler(object):
    @abstractmethod
    def can_handle(self, e):
        pass

    @abstractmethod
    def handle(self, e):
        pass


def register(e):
    # type: (ErrorHandler)->None
    _error_handlers.append(e)


class DefaultErrorHandler(ErrorHandler):
    def can_handle(self, e):
        return True

    def handle(self, ex):
        logger = logging.getLogger(__name__)
        logger.error(str(ex) + "\n" + traceback.format_exc())
        logger.error("Request:\n{0}\n{1}\n".format(request.headers,
                                                   request.data))
        logger.info("Provide your own error handler so that "
                    "a better error is produced, check {0}.".format(
            documentation_link('error_handling')))

        add_responder(StatusCodeResponder(http.client.INTERNAL_SERVER_ERROR))
        return ErrorResponse('UNKNOWN_ERROR', "An error occurred!")


class RoutingErrorHandler(ErrorHandler):
    def can_handle(self, e):
        return isinstance(e, RoutingError)

    def handle(self, ie):
        logging.error(str(ie) + "\n" + traceback.format_exc())
        add_responder(StatusCodeResponder(404))
        return str(ie)


_DEFAULT_ERROR_HANDLER = DefaultErrorHandler()
_ROUTING_ERROR_HANDLER = RoutingErrorHandler()


def error_handler(f):
    """
    Default error handler.
     - On server side error shows a message
       'An error occurred!' and returns 500 status code.
     - Also serves well in the case when the resource/task/method
       is not found - returns 404 status code.
    """

    @wraps(f)
    def error_handling_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except RoutingError as ie:
            return _ROUTING_ERROR_HANDLER.handle(ie)
        except Exception as ex:
            for eh in _error_handlers:
                if eh.can_handle(ex):
                    return eh.handle(ex)

            return _DEFAULT_ERROR_HANDLER.handle(ex)

    return error_handling_function
