"""
:mod:`zsl.interface.webservice.performers.task`
-----------------------------------------------
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *  # NOQA
from functools import partial
import logging

from flask import request

from zsl import Injected, Zsl, inject
from zsl.application.error_handler import error_handler
from zsl.interface.web.utils.execution import convert_to_web_response, execute_web_task, notify_responders
from zsl.interface.web.utils.request_data import extract_data
from zsl.interface.web.utils.response_headers import append_headers
from zsl.router.task import TaskConfiguration, TaskRouter
from zsl.task.job_context import JobContext, WebJobContext


@inject(task_router=TaskRouter)
@append_headers
@notify_responders
@convert_to_web_response
@error_handler
def perform_web_task(namespace, path, task_router=Injected):
    logging.getLogger(__name__).debug("Performing task %s.", path)
    jc = WebJobContext(path, extract_data(request), None, None, request)
    (task, task_callable) = task_router.route(namespace + '/' + path)
    return execute_web_task(jc, lambda: task_callable(jc.task_data))


@inject(app=Zsl, task_configuration=TaskConfiguration)
def create_task_mapping(app, task_configuration):
    # type: (Zsl, TaskConfiguration)->None
    for namespace_configuration in task_configuration.namespaces:
        namespace = namespace_configuration.namespace.rstrip('/')
        f = partial(perform_web_task, namespace)
        f.__name__ = "perform-web-task-{0}".format(namespace)
        app.route("/{0}/<path:path>".format(namespace), methods=["POST", "GET", "OPTIONS"])(f)
