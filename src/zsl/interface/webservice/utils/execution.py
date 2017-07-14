from functools import wraps
from typing import Any, Callable

from flask import request
from flask.helpers import make_response
from flask.wrappers import Response

from zsl import Zsl, inject
from zsl.application.error_handler import error_handler
from zsl.interface.webservice.utils.response_headers import append_headers
from zsl.task.job_context import JobContext, WebJobContext


def notify_responders(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        response = f(*args, **kwargs)
        job_context = JobContext.get_current_context()
        job_context.notify_responders(response)
        return response

    return wrapper


def create_web_response(result):
    # type:(Any,WebJobContext)->Response
    return make_response(result)


def convert_to_web_response(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        return create_web_response(result)

    return wrapper


@append_headers
@notify_responders
@convert_to_web_response
@error_handler
@inject(app=Zsl)
def execute_web_task(job_context, callable, app):
    # type:(WebJobContext,Callable,Zsl)->Response
    app.logger.debug("Data found '%s'.", str(job_context.task_data.get_data()))
    JobContext.set_current_context(job_context)
    if request.method == 'OPTIONS':
        return app.make_default_options_response()
    else:
        return callable()
