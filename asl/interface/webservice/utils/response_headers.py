'''
Created on 25.11.2014

@author: Martin Babka
'''
from asl.application.service_application import service_application
from flask import Response
from flask.helpers import make_response
from functools import wraps

conf = service_application.config

def append_origin(response):
    if conf.get('ALLOW_ORIGIN'):
        response.headers['Access-Control-Allow-Origin'] = conf.get('ALLOW_ORIGIN')
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'accept, origin, content-type'

def append_asl(response):
    response.headers['ASL-Flask-Layer'] = service_application.get_version()

def append_cache(response):
    response.headers['Cache-Control'] = 'no-cache'

def append_all(response):
    append_asl(response)
    append_cache(response)
    append_origin(response)

def headers_appender(f):

    @wraps(f)
    def _response_decorator(*args, **kwargs):
        r = f(*args, **kwargs)
        response = r if isinstance(r, Response) else make_response(r)
        append_all(response)
        return response

    return _response_decorator
