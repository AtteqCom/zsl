'''
Created on 25.11.2014

.. moduleauthor:: Martin Babka
'''
from asl.interface.webservice.utils.response_headers import headers_appender
from asl.interface.webservice.utils.error_handler import error_handler
from asl.application.service_application import service_application
from asl.db.model.app_model_json_encoder import AppModelJSONEncoder
import json
from flask.wrappers import Response

@headers_appender
def default_web_responder(rv):
    if isinstance(rv, Response):
        return rv
    return Response(json.dumps(rv, cls = AppModelJSONEncoder), mimetype="application/json")

def identity_responder(rv):
    return rv

def set_default_responder(responder):
    global _default_responder_method
    _default_responder_method = responder

_default_responder_method = default_web_responder

class Performer(object):
    def __init__(self, f):
        global _default_responder_method
        self._f = f
        self.__name__ = "method-router-performer-of-" + f.__name__
        self.__doc__ = f.__doc__ if hasattr(f, '__doc__') else None
        self.set_responder(_default_responder_method)

    def set_responder(self, responder):
        self._responder = responder

    def _call_inner_function(self, a, kw):
        return self._f(*a, **kw)

    @error_handler
    def __call__(self, *a, **kw):
        rv = self._call_inner_function(a, kw)
        responder = self._responder
        return responder(rv)

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
