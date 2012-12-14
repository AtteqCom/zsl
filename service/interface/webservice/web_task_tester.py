from application.service_application import service_application
from router import router

app = service_application

class WebTaskTester:
    def performTask(self, path):
        # TODO: Logger "Performing task {0}.".format(path)
        (task, task_callable) = router.route(path)
        return task_callable("empty data")

@app.route("/task/<path:path>")
def performWebTask(path):
    return WebTaskTester().performTask(path)

