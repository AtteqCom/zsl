from asl.application.service_application import service_application
from asl.router import task_router
from flask import request
from flask.helpers import make_response
from asl.task.job_context import JobContext, WebJobContext
from asl.interface.webservice.utils.error_handler import error_handler
from asl.interface.webservice.utils.response_headers import headers_appender

app = service_application

@app.route("/task/<path:path>", methods=["POST", "GET", "OPTIONS"])
@headers_appender
@error_handler
def perform_web_task(path):
    app.logger.debug("Performing task %s.", path)

    response = None
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
    else:
        (task, task_callable) = task_router.route(path)

        data = request.form.to_dict(flat=True)
        if request.json:
            data = request.json

        app.logger.debug("Data found '%s'.", str(data))
        jc = WebJobContext(path, data, task, task_callable, request)
        JobContext.set_current_context(jc)
        response = make_response(task_callable(jc.task_data))
        jc.notify_responders(response)

    return response
