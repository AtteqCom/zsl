"""
:mod:`zsl.interface.webservice.performers.default`
--------------------------------------------------

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""
from __future__ import unicode_literals

import logging

from zsl import inject, Zsl


@inject(app=Zsl)
def create_not_found_mapping(app):
    @app.route("/", defaults={'path': ''})
    @app.route("/<path:path>")
    def not_found_mapping(path):
        """
        Default web request handler. Only returns 404 status code.
        """

        response_str = "404 Not Found: path '{0}' was not mapped.".format(path)
        logging.warning(response_str)
        return response_str, 404
