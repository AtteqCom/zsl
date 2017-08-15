"""
:mod:`zsl.interface.webservice.performers.resource`
---------------------------------------------------
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *
import json
import logging

from flask import Response, request
from future.utils import viewitems

from zsl import Zsl, inject
from zsl.application.error_handler import error_handler
from zsl.constants import MimeType
from zsl.db.model import AppModelJSONEncoder
from zsl.interface.resource import ResourceResult
from zsl.interface.web.utils.execution import convert_to_web_response, notify_responders
from zsl.interface.web.utils.response_headers import append_headers
from zsl.task.job_context import WebJobContext
from zsl.utils.request_helper import args_to_dict
from zsl.utils.resource_helper import get_resource_task, parse_resource_path


@inject(app=Zsl)
def create_resource_mapping(app):
    @app.route("/resource/<path:path>",
               methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'])
    @append_headers
    @convert_to_web_response
    @error_handler
    def perform_resource(path):
        logging.debug("Getting resource %s.", path)
        WebJobContext(path, None, None, None, request)

        if request.method == 'OPTIONS':
            response = app.make_default_options_response()
        else:
            (resource, params) = parse_resource_path(path)
            resource_task = get_resource_task(resource)
            if resource_task is None:
                raise ImportError("No resource named '{0}'.".format(resource))
            msg_format = "Fetched resource named '{0}' with data\n{1}."
            logging.debug(msg_format.format(resource, request.data))

            data = request.get_json() if request.data else None

            resource_result = resource_task(params=params,
                                            args=args_to_dict(request.args),
                                            data=data)

            if not isinstance(resource_result, ResourceResult):
                resource_result = ResourceResult(body=resource_result)

            response = Response(
                json.dumps(resource_result.body, cls=AppModelJSONEncoder),
                mimetype=MimeType.APPLICATION_JSON.value)

            if resource_result.status:
                response.status = str(resource_result.status)

            if resource_result.location:
                response.location = resource_result.location

            if resource_result.count is not None:
                response.headers['X-Total-Count'] = resource_result.count

            if resource_result.links:
                response.headers['Links'] = ', '.join(
                    ['<{url}>; rel="{name}"'.format(url=url, name=name)
                     for name, url in viewitems(resource_result.links)]
                )

        return response
