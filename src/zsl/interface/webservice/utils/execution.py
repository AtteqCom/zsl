from flask import request
from flask.helpers import make_response

from zsl import Zsl, inject
from zsl.interface.webservice.utils.error_handler import error_handler
from zsl.interface.webservice.utils.response_headers import append_headers
from zsl.task.job_context import JobContext


@append_headers
@error_handler
@inject(app=Zsl)
def execute_web_task(jc, callable, app):
    if request.method == 'OPTIONS':
        return app.make_default_options_response()
    app.logger.debug("Data found '%s'.", str(jc.task_data.get_data()))
    JobContext.set_current_context(jc)
    response = make_response(callable())
    jc.notify_responders(response)
    return response
