from zsl.application.service_application import service_application as app
from flask import request, Response
from zsl.utils.resource_helper import parse_resource_path, get_resource_task
import json
from zsl.db.model import AppModelJSONEncoder
from zsl.interface.webservice.utils.error_handler import error_handler
from zsl.interface.webservice.utils.response_headers import append_headers
from zsl.utils.request_helper import args_to_dict


@app.route("/resource/<path:path>", methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
@append_headers
@error_handler
def perform_resource(path):
    app.logger.debug("Getting resource %s.", path)

    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
    else:
        (resource, params) = parse_resource_path(path)
        resource_task = get_resource_task(resource)
        if resource_task is None:
            raise ImportError("No resource named {0}.".format(resource))
        app.logger.debug("Fetched resource named {0} with data\n{1}.".format(resource, request.data))

        data = request.json
        rv = resource_task(params=params, args=args_to_dict(request.args), data=data)
        response = Response(json.dumps(rv, cls=AppModelJSONEncoder), mimetype="application/json")

    return response
