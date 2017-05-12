"""
:mod:`zsl.interface.webservice.performers.resource`
---------------------------------------------------
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
from future.utils import viewitems

import json
import logging

from flask import request, Response

from zsl import Zsl, inject
from zsl.db.model import AppModelJSONEncoder
from zsl.interface.webservice.utils.error_handler import error_handler
from zsl.interface.webservice.utils.response_headers import append_headers
from zsl.utils.request_helper import args_to_dict
from zsl.utils.resource_helper import parse_resource_path, get_resource_task
from zsl.interface.resource import ResourceResult


def create_response_from_pure_result(result):
    # type: (Any) -> Response

    return Response(json.dumps(result, cls=AppModelJSONEncoder), mimetype="application/json")


def create_response_from_resource_result(result):
    # type: (ResourceResult) -> Response
    response = create_response_from_pure_result(result.body)

    if result.count is not None:
        response.headers['X-Total-Count'] = result.count
        response.headers['Access-Control-Expose-Headers'] = 'X-Total-Count'


@inject(app=Zsl)
def create_resource_mapping(app):
    @app.route("/resource/<path:path>", methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'])
    @append_headers
    @error_handler
    def perform_resource(path):
        logging.debug("Getting resource %s.", path)

        if request.method == 'OPTIONS':
            response = app.make_default_options_response()
        else:
            (resource, params) = parse_resource_path(path)
            resource_task = get_resource_task(resource)
            if resource_task is None:
                raise ImportError("No resource named {0}.".format(resource))
            logging.debug("Fetched resource named {0} with data\n{1}.".format(resource, request.data))

            data = request.get_json() if request.data else None

            rv = resource_task(params=params, args=args_to_dict(request.args), data=data)

            if not isinstance(rv, ResourceResult):
                rv = ResourceResult(body=rv)

            response = Response(json.dumps(rv.body, cls=AppModelJSONEncoder), mimetype="application/json")

            if rv.status:
                response.status = str(rv.status)

            if rv.location:
                response.location = rv.location

            if rv.count is not None:
                response.headers['X-Total-Count'] = rv.count

            if rv.links:
                response.headers['Links'] = ', '.join(
                    ['<{url}>; rel="{name}"'.format(url=url, name=name)
                     for name, url in viewitems(rv.links)]
                )

        return response
