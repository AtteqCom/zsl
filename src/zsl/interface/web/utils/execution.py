from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *  # NOQA
from functools import wraps
from typing import Any, Callable

from flask import request
from flask.helpers import make_response
from flask.wrappers import Response

from zsl import Zsl, inject
from zsl.task.job_context import JobContext, WebJobContext


def notify_responders(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        response = f(*args, **kwargs)
        job_context = JobContext.get_current_context()
        job_context.notify_responders(response)
        return response

    return wrapper


def convert_to_web_response(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        return _create_web_response(result)

    return wrapper


def _create_web_response(result):
    # type:(Any,WebJobContext)->Response
    return make_response(result)


@inject(app=Zsl)
def execute_web_task(job_context, callable, app):
    # type:(WebJobContext, Callable, Zsl)->Response
    app.logger.debug("Data found '%s'.", str(job_context.task_data.payload))
    if request.method == 'OPTIONS':
        return app.make_default_options_response()
    else:
        return callable()
