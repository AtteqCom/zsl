"""
:mod:`zsl.interface.webservice.utils.response_headers`
------------------------------------------------------

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""
from __future__ import unicode_literals

from functools import wraps

from flask import Response
from flask.helpers import make_response

from zsl import Config, Zsl, inject
from zsl.task.task_decorator import CrossdomainWebTaskResponder


@inject(config=Config)
def append_crossdomain(response, config):
    # type: (Response, Config)->None
    """
    Adds the default crossdomain headers.
    Uses the :class:`zsl.task.task_decorator.CrossdomainWebTaskResponder`
    to generate the headers.

    :param response: Current web response.
    :param config:  Current configuration.
    """
    # The CORS has already been setup.
    if 'Access-Control-Allow-Origin' in response.headers:
        return
    CrossdomainWebTaskResponder().respond(response)


@inject(app=Zsl)
def append_asl(response, app):
    response.headers['ZSL'] = app.get_version()


def append_cache(response):
    response.headers['Cache-Control'] = 'no-cache'


def append_all(response):
    append_asl(response)
    append_cache(response)
    append_crossdomain(response)


def append_headers(f):
    """
    Appends all the web headers:
      * ZSL version and information,
      * default CORS if not already set up,
      * cache.

    :param f: The decorated function.
    :return: The function which appends the web headers.
    """
    @wraps(f)
    def _response_decorator(*args, **kwargs):
        r = f(*args, **kwargs)
        response = r if isinstance(r, Response) else make_response(r)
        append_all(response)
        return response

    return _response_decorator
