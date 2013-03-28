from application.service_application import service_application
from router import router
from flask import request
from task.task_data import TaskData
from flask.helpers import make_response

app = service_application

class WebTaskTester:
    def performTask(self, path):
        app.logger.debug("Performing task %s.", path)
        (task, task_callable) = router.route(path)

        data = request.data
        if request.headers.has_key("Content-Type") and request.headers["Content-Type"] == "application/json":
            data = request.json

        app.logger.debug("Data found '%s'.", data)
        data = TaskData(app, data)

        response = make_response(task_callable(data))

        # TODO: How to handle this?
        #if 'Origin' in request.headers:
        #    response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
        #else:
        #    response.headers['Access-Control-Allow-Origin'] = '*'

        response.headers['ASL-Flask-Layer'] = '1.00aa0'
        response.headers['Cache-Control'] = 'no-cache';

        return response

@app.route("/task/<path:path>", methods=["POST", "GET"])
def perform_web_task(path):
    return WebTaskTester().performTask(path)
