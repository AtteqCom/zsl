"""
:mod:`zsl.router.method`
------------------------

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""
from __future__ import unicode_literals
from builtins import object
from zsl.interface.webservice.utils.response_headers import append_headers
from zsl.interface.webservice.utils.error_handler import error_handler
from zsl.db.model.app_model_json_encoder import AppModelJSONEncoder
import json
from flask.wrappers import Response

from zsl import inject, Config, Zsl, Injected


@append_headers
def default_web_responder(rv):
    if isinstance(rv, Response):
        return rv
    return Response(json.dumps(rv, cls=AppModelJSONEncoder), mimetype="application/json")


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
        self._responder = None
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


# TODO this is a blind refactor, should be redone utilizing DI from the start
@inject(app=Zsl)
def route(path, app=Injected, **options):
    def _decorator(f):
        routed_function = app.route("/method" + path, **options)
        return routed_function(Performer(f))

    return _decorator


@inject(config=Config)
def get_method_packages(config):
    method_package = config.get('METHOD_PACKAGE')
    if method_package is None:
        return ()

    return method_package if isinstance(method_package, list) else (method_package,)
