"""
:mod:`zsl.interface.webservice.performers.task`
-----------------------------------------------
"""
from __future__ import unicode_literals
from builtins import str
from flask import request
from flask.helpers import make_response

from zsl import inject, Zsl, Injected
from zsl.interface.webservice.utils.request_data import extract_data
from zsl.task.job_context import JobContext, WebJobContext
from zsl.interface.webservice.utils.error_handler import error_handler
from zsl.interface.webservice.utils.response_headers import append_headers
from zsl.router.task import TaskRouter


@inject(app=Zsl)
def create_web_task(app):
    @app.route("/task/<path:path>", methods=["POST", "GET", "OPTIONS"])
    @append_headers
    @error_handler
    @inject(task_router=TaskRouter)
    def perform_web_task(path, task_router=Injected):
        app.logger.debug("Performing task %s.", path)
        if request.method == 'OPTIONS':
            response = app.make_default_options_response()
        else:
            (task, task_callable) = task_router.route(path)
            data = extract_data(request)
            app.logger.debug("Data found '%s'.", str(data))
            jc = WebJobContext(path, data, task, task_callable, request)
            JobContext.set_current_context(jc)
            response = make_response(task_callable(jc.task_data))
            jc.notify_responders(response)

        return response
