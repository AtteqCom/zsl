from asl.application.service_application import service_application
from flask import request
from flask.helpers import make_response
from asl.task.task_data import TaskData
from asl.utils.resource_helper import parse_resource_path, get_resource_task
import json

app = service_application

@app.route("/resource/<path:path>", methods=['GET', 'POST', 'PUT', 'DELETE'])
def perform_resource(path):
    app.logger.debug("Getting resource %s.", path)
    (resource, param) = parse_resource_path(path)

    resource_task = get_resource_task(resource)

    if resource_task == None:
        # TODO what?
        return

    data = request.data
    if request.headers.has_key("Content-Type") and request.headers["Content-Type"] == "application/json":
        data = request.json

    data = TaskData(app, data)


    response = make_response(json.dumps(resource_task(data=data, param=param)))

    response.headers['ASL-Flask-Layer'] = '1.00aa0'
    response.headers['Cache-Control'] = 'no-cache';

    return response