'''
Created on 25.11.2014

@author: Martin Babka
'''
from asl.interface.webservice.utils.response_headers import headers_appender
from asl.interface.webservice.utils.error_handler import error_handler
from asl.application.service_application import service_application
from asl.db.model.app_model_json_encoder import AppModelJSONEncoder
import json

class Performer(object):
    def __init__(self, f):
        self._f = f
        self.__name__ = "method-router-performer-of-" + f.__name__

    @headers_appender
    @error_handler
    def __call__(self, *a, **kw):
        rv = self._f(*a, **kw)
        return json.dumps(rv, cls = AppModelJSONEncoder)

def route(path, **options):
    def _decorator(f):
        routed_function = service_application.route("/method" + path, **options)
        return routed_function(Performer(f))

    return _decorator

def get_method_packages():
    method_package = service_application.config.get('METHOD_PACKAGE')
    if method_package is None:
        return ()

    return method_package if isinstance(method_package, list) else (method_package,)
