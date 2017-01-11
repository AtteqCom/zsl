"""
:mod:`asl.interface.webservice.performers.default`

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""
from __future__ import unicode_literals
from zsl.application.service_application import service_application as app


@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def not_found_mapping(path):
    """
    Default web request handler. Only returns 404 status code.
    """
    
    response_str = "Default handler, not found! Path not found '{0}'.".format(path)
    app.logger.warn(response_str)
    return response_str, 404
