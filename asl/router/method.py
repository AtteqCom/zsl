'''
Created on 25.11.2014

@author: Martin Babka
'''
from asl.interface.webservice.utils.response_headers import headers_appender
from asl.interface.webservice.utils.error_handler import error_handler
from asl.application.service_application import service_application
from asl.db.model.app_model_json_encoder import AppModelJSONEncoder
import json


def route(path, **options):
    routed_function = service_application.route("/method" + path, **options)

    def _decorator(f):
        def _encode(f):
            def _wrapper(*a, **kw):
                rv = f(*a, **kw)
                return json.dumps(rv, cls = AppModelJSONEncoder)
            return _wrapper
        return routed_function(headers_appender(error_handler(_encode(f))))

    return _decorator

def get_method_packages():
    method_package = service_application.config.get('METHOD_PACKAGE')
    if method_package is None:
        return ()

    return method_package if isinstance(method_package, list) else (method_package,)
