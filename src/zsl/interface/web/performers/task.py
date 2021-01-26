"""
:mod:`zsl.interface.webservice.performers.task`
-----------------------------------------------
"""

from functools import partial
import logging

from flask import request
from flask.wrappers import Response

from zsl import Zsl, inject
from zsl.application.error_handler import error_handler
from zsl.interface.web.utils.execution import convert_to_web_response, execute_web_task, notify_responders
from zsl.interface.web.utils.request_data import extract_data
from zsl.interface.web.utils.response_headers import append_headers
from zsl.router.task import TaskConfiguration, TaskRouter
from zsl.task.job_context import JobContext, WebJobContext


@inject
@append_headers
@notify_responders
@convert_to_web_response
@error_handler
def perform_web_task(namespace: str, path: str, task_router: TaskRouter) -> Response:
    logging.getLogger(__name__).debug("Performing task %s.", path)
    jc = WebJobContext(path, extract_data(request), None, None, request)
    (task, task_callable) = task_router.route(namespace + '/' + path)
    return execute_web_task(jc, lambda: task_callable(jc.task_data))


@inject
def create_task_mapping(app: Zsl, task_configuration: TaskConfiguration) -> None:
    # type: (Zsl, TaskConfiguration)->None
    for namespace_configuration in task_configuration.namespaces:
        namespace = namespace_configuration.namespace.rstrip('/')

        f = partial(perform_web_task, namespace)
        name = "perform-web-task-{}".format(namespace)
        f.__name__ = name

        logging.getLogger(__name__).debug("Registering {} at /{}".format(name, namespace))
        app.add_url_rule("/{}/<path:path>".format(namespace), name, f, methods=["POST", "GET", "OPTIONS"])
