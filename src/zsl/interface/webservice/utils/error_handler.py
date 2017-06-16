"""
:mod:`zsl.interface.webservice.utils.error_handler`
---------------------------------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals
from builtins import str
from builtins import object

import traceback
import logging
from functools import wraps
from abc import abstractmethod

from flask import request

_error_handlers = []


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


def error_handler(f):
    """
    Default error handler.
     - On server side error shows a message 'An error occurred!' and returns 500 status code.
     - Also serves well in the case when the resource/task/method is not found - returns 404 status code.
    """

    @wraps(f)
    def error_handling_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ImportError as ie:
            logging.error(str(ie) + "\n" + traceback.format_exc())
            return str(ie), 404
        except Exception as ex:
            for eh in _error_handlers:
                if eh.can_handle(ex):
                    return eh.handle(ex)

            logging.error(str(ex) + "\n" + traceback.format_exc())
            logging.error("Request:\n{0}\n{1}\n".format(request.headers, request.data))

            return "An error occurred!", 500

    return error_handling_function
