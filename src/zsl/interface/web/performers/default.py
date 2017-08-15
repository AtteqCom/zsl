"""
:mod:`zsl.interface.webservice.performers.default`
--------------------------------------------------

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""
from __future__ import unicode_literals

from flask.globals import request

from zsl import Zsl, inject
from zsl.application.error_handler import error_handler
from zsl.interface.web.utils.execution import convert_to_web_response, notify_responders
from zsl.interface.web.utils.response_headers import append_headers
from zsl.router.task import RoutingError
from zsl.task.job_context import WebJobContext


@inject(app=Zsl)
def create_not_found_mapping(app):
    @app.route("/", defaults={'path': ''})
    @app.route("/<path:path>")
    @append_headers
    @notify_responders
    @convert_to_web_response
    @error_handler
    def not_found_mapping(path):
        """
        Default web request handler. Only returns 404 status code.
        """
        WebJobContext(path, None, None, None, request)
        raise RoutingError(path)
