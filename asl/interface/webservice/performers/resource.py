from asl.application.service_application import service_application
from flask import request, Response
#from asl.task.task_data import TaskData
from asl.utils.resource_helper import parse_resource_path, get_resource_task
import json
from asl.db.model import AppModelJSONEncoder
from asl.interface.webservice.utils.error_handler import error_handler
from asl.interface.webservice.utils.response_headers import headers_appender
from asl.utils.request_helper import args_to_dict

app = service_application
conf = service_application.config

@app.route("/resource/<path:path>", methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
@headers_appender
@error_handler
def perform_resource(path):
    app.logger.debug("Getting resource %s.", path)

    response = None
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
    else:
        (resource, params) = parse_resource_path(path)
        resource_task = get_resource_task(resource)
        if resource_task == None:
            raise ImportError("No resource named {0}.".format(resource))

        data = request.json
        rv = resource_task(params=params, args=args_to_dict(request.args), data=data)
        response = Response(json.dumps(rv, cls = AppModelJSONEncoder), mimetype="application/json")

    return response
