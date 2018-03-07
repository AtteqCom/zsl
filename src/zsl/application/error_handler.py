"""
:mod:`zsl.application.error_handler`
---------------------------------------------------

This module does the error handling. It allows users to register
an error handler for a given exception type. It also provides default
error handlers.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *
from functools import wraps
import http.client
import logging
import traceback
from typing import List

from flask import request

from zsl import inject
from zsl.db.model.app_model import AppModel
from zsl.errors import ErrorConfiguration, ErrorHandler, ErrorProcessor
from zsl.interface.task import ModelConversionError
from zsl.router.task import RoutingError
from zsl.task.job_context import JobContext, StatusCodeResponder, WebJobContext, add_responder
from zsl.task.task_decorator import json_output
from zsl.utils.documentation import documentation_link
from zsl.utils.http import get_http_status_code_value


class ErrorResponse(AppModel):
    def __init__(self, code, message):
        super(ErrorResponse, self).__init__({})
        self.code = code
        self.message = message


def register(e):
    # type: (ErrorHandler|ErrorProcessor)->None
    if isinstance(e, ErrorHandler):
        _error_handlers.append(e)
    if isinstance(e, ErrorProcessor):
        _error_processors.append(e)


class DefaultErrorHandler(ErrorHandler):
    ERROR_CODE = "UNKNOWN_ERROR"
    ERROR_MESSAGE = "An error occurred!"

    def can_handle(self, e):
        return True

    @json_output
    def handle(self, ex):
        logger = logging.getLogger(__name__)
        logger.error(str(ex) + "\n" + traceback.format_exc())
        logger.error("Request:\n{0}\n{1}\n".format(request.headers,
                                                   request.data))
        link = documentation_link('error_handling')
        logger.info("Provide your own error handler so that "
                    "a better error is produced, check {0}.".format(link))

        add_responder(StatusCodeResponder(http.client.INTERNAL_SERVER_ERROR))
        return ErrorResponse(self.ERROR_CODE, self.ERROR_MESSAGE)


class RoutingErrorHandler(ErrorHandler):
    ERROR_CODE = 'NOT_FOUND'

    def can_handle(self, e):
        return isinstance(e, RoutingError)

    @json_output
    def handle(self, ie):
        logging.error(str(ie) + "\n" + traceback.format_exc())
        add_responder(StatusCodeResponder(get_http_status_code_value(http.client.NOT_FOUND)))
        return ErrorResponse(self.ERROR_CODE, str(ie))


class ModelConversionErrorHandler(ErrorHandler):
    ERROR_CODE = 'INVALID_REQUEST'

    def can_handle(self, e):
        return isinstance(e, ModelConversionError)

    @json_output
    def handle(self, e):
        logging.error(str(e) + "\n" + traceback.format_exc())
        add_responder(StatusCodeResponder(get_http_status_code_value(http.client.UNPROCESSABLE_ENTITY)))
        return ErrorResponse(self.ERROR_CODE, str(e))


_DEFAULT_ERROR_HANDLER = DefaultErrorHandler()
_ROUTING_ERROR_HANDLER = RoutingErrorHandler()
_MODEL_CONVERSION_ERROR_HANDLER = ModelConversionErrorHandler()
_error_handlers = [_MODEL_CONVERSION_ERROR_HANDLER, _ROUTING_ERROR_HANDLER]  # type: List[ErrorHandler]
_error_processors = []


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
        @inject(error_config=ErrorConfiguration)
        def get_error_configuration(error_config):
            # type:(ErrorConfiguration)->ErrorConfiguration
            return error_config

        def should_skip_handling():
            use_flask_handler = get_error_configuration().use_flask_handler
            is_web_request = isinstance(JobContext.get_current_context(), WebJobContext)
            return use_flask_handler and is_web_request

        try:
            return f(*args, **kwargs)
        except Exception as ex:
            if should_skip_handling():
                raise

            for ep in _error_processors:
                ep.handle(ex)

            for eh in _error_handlers:
                if eh.can_handle(ex):
                    return eh.handle(ex)

            return _DEFAULT_ERROR_HANDLER.handle(ex)

    return error_handling_function
