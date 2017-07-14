"""
:mod:`zsl.interface.webservice.performers.task`
-----------------------------------------------
"""
from __future__ import unicode_literals
from builtins import *

import logging

from flask import request

from zsl import inject, Zsl, Injected
from zsl.interface.webservice.utils.execution import execute_web_task
from zsl.interface.webservice.utils.request_data import extract_data
from zsl.task.job_context import WebJobContext
from zsl.router.task import TaskRouter


@inject(app=Zsl)
def create_web_task(app):
    @app.route("/task/<path:path>", methods=["POST", "GET", "OPTIONS"])
    @inject(task_router=TaskRouter)
    def perform_web_task(path, task_router=Injected):
        logging.getLogger(__name__).debug("Performing task %s.", path)
        (task, task_callable) = task_router.route(path)
        jc = WebJobContext(path, extract_data(request), task, task_callable, request)
        return execute_web_task(jc, lambda: task_callable(jc.task_data))
