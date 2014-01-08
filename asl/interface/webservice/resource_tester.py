from asl.application.service_application import service_application
from flask import request, Response
#from asl.task.task_data import TaskData
from asl.utils.resource_helper import parse_resource_path, get_resource_task
import json
from asl.db.model import AppModelJSONEncoder
import traceback

app = service_application

def args_to_dict(args):
    return dict((key, value[0]) for key, value in dict(args).items())

@app.route("/resource/<path:path>", methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def perform_resource(path):
    try:
        app.logger.debug("Getting resource %s.", path)
        (resource, params) = parse_resource_path(path)

        resource_task = get_resource_task(resource)

        if resource_task == None:
            # TODO what?
            return

        data = request.json

        rv = resource_task(params=params, args=args_to_dict(request.args), data=data)
        response = Response(json.dumps(rv, cls = AppModelJSONEncoder), mimetype="application/json")

        response.headers['ASL-Flask-Layer'] = '1.00aa0'
        response.headers['Cache-Control'] = 'no-cache';
        return response
    except Exception as e:
        app.logger.error(str(e) + "\n" + traceback.format_exc())
        raise
