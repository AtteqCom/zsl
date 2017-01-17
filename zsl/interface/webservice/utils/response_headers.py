"""
:mod:`zsl.interface.webservice.utils.response_headers`
------------------------------------------------------

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""
from __future__ import unicode_literals
from zsl.application.service_application import service_application
from flask import Response
from flask.helpers import make_response
from functools import wraps


def append_crossdomain(response):
    conf = service_application.config

    # The CORS has already been setup.
    if 'Access-Control-Allow-Origin' in response.headers:
        return

    if conf.get('ALLOW_ORIGIN'):
        response.headers['Access-Control-Allow-Origin'] = conf.get('ALLOW_ORIGIN')
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'accept, origin, content-type'


def append_asl(response):
    response.headers['ASL-Flask-Layer'] = service_application.get_version()


def append_cache(response):
    response.headers['Cache-Control'] = 'no-cache'


def append_all(response):
    append_asl(response)
    append_cache(response)
    append_crossdomain(response)


def append_headers(f):

    @wraps(f)
    def _response_decorator(*args, **kwargs):
        r = f(*args, **kwargs)
        response = r if isinstance(r, Response) else make_response(r)
        append_all(response)
        return response

    return _response_decorator
