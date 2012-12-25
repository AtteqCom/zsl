from application.service_application import service_application
from router import router
from flask import request
from task.task_data import TaskData

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
        return task_callable(data)

@app.route("/task/<path:path>", methods=["POST", "GET"])
def performWebTask(path):
    return WebTaskTester().performTask(path)
