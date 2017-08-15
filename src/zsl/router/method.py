"""
:mod:`zsl.router.method`
------------------------

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""
from __future__ import unicode_literals

from builtins import *
import json
import logging

from flask import request
from flask.wrappers import Response

from zsl import Config, Injected, Zsl, inject
from zsl.application.error_handler import error_handler
from zsl.application.modules.web.configuration import MethodConfiguration
from zsl.constants import MimeType
from zsl.db.model.app_model_json_encoder import AppModelJSONEncoder
from zsl.interface.web.utils.execution import convert_to_web_response, execute_web_task, notify_responders
from zsl.interface.web.utils.request_data import extract_data
from zsl.interface.web.utils.response_headers import append_headers
from zsl.task.job_context import WebJobContext

METHOD_CONFIG_NAME = 'METHOD'


@append_headers
def default_web_responder(rv):
    if isinstance(rv, Response):
        return rv
    return Response(json.dumps(rv, cls=AppModelJSONEncoder),
                    mimetype=MimeType.APPLICATION_JSON.value)


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
        self.__name__ = "zsl-method-router-performer-of-" + f.__name__
        self.__doc__ = f.__doc__ if hasattr(f, '__doc__') else None
        self._responder = None
        self.set_responder(_default_responder_method)

    def set_responder(self, responder):
        self._responder = responder

    def _call_inner_function(self, a, kw):
        return self._f(*a, **kw)

    @append_headers
    @notify_responders
    @convert_to_web_response
    @error_handler
    def __call__(self, *a, **kw):
        def task_callable():
            return self._call_inner_function(a, kw)

        jc = WebJobContext(None, extract_data(request), task_callable,
                           task_callable, request)
        return execute_web_task(jc, task_callable)


def _get_method_configuration(config):
    # type: (Config) -> MethodConfiguration
    return config.get(METHOD_CONFIG_NAME, MethodConfiguration())


@inject(app=Zsl, config=Config)
def route(path, app=Injected, config=Injected, **options):
    def _decorator(f):
        method_config = _get_method_configuration(config)
        url = "/{0}{1}".format(method_config.url_prefix, path)
        logging.getLogger(__name__).info(
            "Mapping url '{0}' as a method.".format(url))
        routed_function = app.route(url, **options)
        return routed_function(Performer(f))

    return _decorator


@inject(config=Config)
def get_method_packages(config):
    return _get_method_configuration(config).packages
