"""
:mod:`zsl.task.task_decorator`
------------------------------

.. moduleauthor:: Martin Babka <babka@atteq.com>,
                  Peter Morihladko <morihladko@atteq.com>,
                  Jan Janco <janco@atteq.com>,
                  Lubos Pis <pis@atteq.com>
"""
from __future__ import unicode_literals

from builtins import *
from datetime import timedelta
from functools import wraps
import json
import logging
from os.path import os
import traceback
from typing import Callable, List, Union

from flask import request

from zsl import Config, Injected, Zsl, inject
from zsl.application.modules.web.cors import CORSConfiguration
from zsl.constants import MimeType
from zsl.db.model import AppModelJSONEncoder
from zsl.task.job_context import JobContext, Responder, WebJobContext, add_responder
from zsl.task.task_data import TaskData
from zsl.utils.file_helper import makedirs
from zsl.utils.security_helper import verify_security_data
from zsl.utils.string_helper import join_list


def log_output(f):
    """
    Logs the output value.
    """

    @wraps(f)
    def wrapper_fn(*args, **kwargs):
        res = f(*args, **kwargs)
        logging.debug("Logging result %s.", res)
        return res

    return wrapper_fn


def save_to_file(destination_filename, append=False):
    """
    Save the output value to file.
    """

    def decorator_fn(f):
        @wraps(f)
        def wrapper_fn(*args, **kwargs):
            res = f(*args, **kwargs)

            makedirs(os.path.dirname(destination_filename))
            mode = "a" if append else "w"
            with open(destination_filename, mode) as text_file:
                text_file.write(res)

            return res

        return wrapper_fn

    return decorator_fn


def json_input(f):
    """
    Expects task input data in json format and parse this data.
    """

    @wraps(f)
    def json_input_decorator(*args, **kwargs):
        # If the data is already transformed, we do not transform it any
        # further.
        task_data = _get_data_from_args(args)

        if task_data is None:
            logging.error("Task data is empty during JSON decoding.")

        if task_data.payload:
            try:
                is_transformed = request.get_json()

                # We transform the data only in the case of plain POST requests.
                if not is_transformed:
                    task_data.transform_payload(json.loads)
            except (ValueError, RuntimeError):
                logging.error(
                    "Exception while processing JSON input decorator.")
                task_data.transform_payload(json.loads)
        else:
            task_data.transform_payload(lambda _: {})

        return f(*args, **kwargs)

    return json_input_decorator


def json_output(f):
    """
    Format response to json and in case of web-request set response content type
    to 'application/json'.
    """

    @wraps(f)
    def json_output_decorator(*args, **kwargs):
        @inject(config=Config)
        def get_config(config):
            return config

        config = get_config()

        rv = f(*args, **kwargs)
        indent = None
        if config.get('DEBUG', False):
            logging.getLogger(__name__).debug("Formatting JSON nicely.")
            indent = 2
        rv = json.dumps(rv, cls=AppModelJSONEncoder, indent=indent)
        _set_json_response_content_type()
        return rv

    return json_output_decorator


def _set_json_response_content_type():
    responder = MimeSetterWebTaskResponder(MimeType.APPLICATION_JSON.value)
    add_responder(responder)


def jsonp_wrap(callback_key='callback'):
    """
    Format response to jsonp and add a callback to JSON data - a jsonp request
    """

    def decorator_fn(f):

        @wraps(f)
        def jsonp_output_decorator(*args, **kwargs):
            task_data = _get_data_from_args(args)
            data = task_data.get_data()

            if callback_key not in data:
                raise KeyError(
                    'Missing required parameter "{0}" for task.'.format(
                        callback_key))

            callback = data[callback_key]
            jsonp = f(*args, **kwargs)
            if isinstance(JobContext.get_current_context(), WebJobContext):
                JobContext.get_current_context().add_responder(
                    MimeSetterWebTaskResponder('application/javascript'))
            jsonp = "{callback}({data})".format(callback=callback, data=jsonp)

            return jsonp

        return jsonp_output_decorator

    return decorator_fn


def jsend_output(fail_exception_classes=None):
    """
    Format task result to json output in jsend specification format. See:
    http://labs.omniti.com/labs/jsend. Task return value must be dict or None.

    @param fail_exception_classes: exceptions which will produce 'fail' response
    status.
    """

    fail_exception_classes = fail_exception_classes if fail_exception_classes \
        else ()

    def decorator_fn(f):

        @wraps(f)
        @json_output
        def jsend_output_decorator(*args, **kwargs):
            try:
                rv = f(*args, **kwargs)
            except fail_exception_classes as e:
                return {'status': 'fail', 'data': {'message': str(e)}}
            except Exception as e:
                logging.error(str(e) + "\n" + traceback.format_exc())
                return {'status': 'error', 'message': 'Server error.'}

            if not isinstance(rv, dict) and rv is not None:
                msg = 'jsend_output decorator error: task must return dict ' \
                      'or None.\nTask return value: {0}.'
                logging.error(msg.format(rv))
                return {'status': 'error', 'message': 'Server error.'}

            return {'status': 'success', 'data': rv}

        return jsend_output_decorator

    return decorator_fn


def web_error_and_result(f):
    """
    Same as error_and_result decorator, except:
    If no exception was raised during task execution, ONLY IN CASE OF WEB
    REQUEST formats task result into json dictionary {'data': task return value}
    """

    @wraps(f)
    def web_error_and_result_decorator(*args, **kwargs):
        return error_and_result_decorator_inner_fn(f, True, *args, **kwargs)

    return web_error_and_result_decorator


def error_and_result(f):
    """
    Format task result into json dictionary `{'data': task return value}` if no
    exception was raised during the task execution. If there was raised an
    exception during task execution, formats task result into dictionary
    `{'error': exception message with traceback}`.
    """

    @wraps(f)
    def error_and_result_decorator(*args, **kwargs):
        return error_and_result_decorator_inner_fn(f, False, *args, **kwargs)

    return error_and_result_decorator


def error_and_result_decorator_inner_fn(f, web_only, *args, **kwargs):
    try:
        ret_val = f(*args, **kwargs)
        if web_only and not isinstance(JobContext.get_current_context(),
                                       WebJobContext):
            rv = ret_val
        else:
            rv = {'data': ret_val}
    except:  # NOQA
        exc = traceback.format_exc()
        logging.error(exc)
        rv = {'error': "{0}".format(exc)}

    return json.dumps(rv)


def required_data(*data):
    """
    Task decorator which checks if the given variables (indices) are stored
    inside the task data.
    """

    def decorator_fn(f):

        @wraps(f)
        def required_data_decorator(*args, **kwargs):
            task_data = _get_data_from_args(args).get_data()
            for i in data:
                if i not in task_data:
                    raise KeyError(
                        'Missing required parameter "{0}" for task.'.format(i))

            return f(*args, **kwargs)

        return required_data_decorator

    return decorator_fn


def append_get_parameters(accept_only_web=True):
    # type: (bool) -> Callable
    """
    Task decorator which appends the GET data to the task data.

    :param accept_only_web: Parameter which limits using this task only
                            with web requests.
    """

    def wrapper(f):

        @wraps(f)
        def append_get_parameters_wrapper_fn(*args, **kwargs):
            jc = JobContext.get_current_context()

            if isinstance(jc, WebJobContext):
                # Update the data with GET parameters
                web_request = jc.get_web_request()
                task_data = _get_data_from_args(args)
                data = task_data.get_data()
                data.update(web_request.args.to_dict(flat=True))
            elif accept_only_web:
                # Raise exception on non web usage if necessary
                raise Exception("append_get_parameters decorator may be used "
                                "with GET requests only.")

            return f(*args, **kwargs)

        return append_get_parameters_wrapper_fn

    return wrapper


def web_task(f):
    """
    Checks if the task is called through the web interface.
    Task return value should be in format {'data': ...}.
    """

    @wraps(f)
    def web_task_decorator(*args, **kwargs):
        jc = JobContext.get_current_context()
        if not isinstance(jc, WebJobContext):
            raise Exception(
                "The WebTask is not called through the web interface.")
        data = f(*args, **kwargs)
        jc.add_responder(WebTaskResponder(data))
        return data['data'] if 'data' in data else ""

    return web_task_decorator


def secured_task(f):
    """
    Secured task decorator.
    """

    @wraps(f)
    def secured_task_decorator(*args, **kwargs):
        task_data = _get_data_from_args(args)
        assert isinstance(task_data, TaskData)
        if not verify_security_data(task_data.get_data()['security']):
            raise SecurityException(
                task_data.get_data()['security']['hashed_token'])

        task_data.transform_payload(lambda x: x['data'])
        return f(*args, **kwargs)

    return secured_task_decorator


def xml_output(f):
    """
    Set content-type for response to WEB-REQUEST to 'text/xml'
    """

    @wraps(f)
    def xml_output_inner_fn(*args, **kwargs):
        ret_val = f(*args, **kwargs)

        if isinstance(JobContext.get_current_context(), WebJobContext):
            JobContext.get_current_context().add_responder(
                MimeSetterWebTaskResponder('text/xml'))
        return ret_val

    return xml_output_inner_fn


def file_upload(f):
    """
    Return list of `werkzeug.datastructures.FileStorage` objects - files to be
    uploaded
    """

    @wraps(f)
    def file_upload_decorator(*args, **kwargs):
        # If the data is already transformed, we do not transform it any
        # further.
        task_data = _get_data_from_args(args)

        if task_data is None:
            logging.error("Task data is empty during FilesUploadDecorator.")

        task_data.transform_payload(lambda _: request.files.getlist('file'))
        return f(*args, **kwargs)

    return file_upload_decorator


def _get_data_from_args(args):
    task_data = None
    for d in args:
        if isinstance(d, TaskData):
            task_data = d

    return task_data


class SecurityException(Exception):
    def __init__(self, hashed_token):
        Exception.__init__(self,
                           "Invalid hashed token '{0}'.".format(hashed_token))
        self._hashed_token = hashed_token

    def get_hashed_token(self):
        return self._hashed_token


class WebTaskResponder(Responder):
    def __init__(self, data):
        self.data = data

    def respond(self, response):
        for k in self.data:
            if k == 'headers':
                for header_name in self.data[k]:
                    response.headers[header_name] = self.data[k][header_name]
            else:
                setattr(response, k, self.data[k])


class MimeSetterWebTaskResponder(Responder):
    def __init__(self, mime):
        self._mime = mime

    def respond(self, r):
        r.content_type = self._mime


class CrossdomainWebTaskResponder(Responder):
    """
    source: http://flask.pocoo.org/snippets/56/
    """

    @inject(app=Zsl, cors_config=CORSConfiguration)
    def __init__(self, origin=None, methods=None, allow_headers=None,
                 expose_headers=None, max_age=None, app=Injected,
                 cors_config=Injected):
        # type: (str, List[str], str, str, Union[int, timedelta], Zsl, CORSConfiguration)->None
        self._app = app

        methods = join_list(methods, transform=lambda x: x.upper())
        self.methods = methods

        if allow_headers is None:
            allow_headers = cors_config.allow_headers
        allow_headers = join_list(allow_headers)
        self.allow_headers = allow_headers

        if expose_headers is None:
            expose_headers = cors_config.expose_headers
        expose_headers = join_list(expose_headers)
        self.expose_headers = expose_headers

        if origin is None:
            origin = cors_config.origin
        self.origin = join_list(origin)

        if max_age is None:
            max_age = cors_config.max_age
        if isinstance(max_age, timedelta):
            max_age = max_age.total_seconds()
        self.max_age = max_age

    def get_methods(self):
        if self.methods is not None:
            return self.methods

        options_resp = self._app.make_default_options_response()
        return options_resp.headers['allow']

    def respond(self, response):
        headers = response.headers
        headers['Access-Control-Allow-Origin'] = self.origin
        headers['Access-Control-Allow-Methods'] = self.get_methods()
        headers['Access-Control-Max-Age'] = str(self.max_age)
        headers['Access-Control-Allow-Headers'] = self.allow_headers
        headers['Access-Control-Expose-Headers'] = self.expose_headers
        return response


def crossdomain(origin=None, methods=None, allow_headers=None,
                expose_headers=None, max_age=None):
    def decorator(f):
        @wraps(f)
        def crossdomain_inner_fn(*args, **kwargs):
            responder = CrossdomainWebTaskResponder(
                origin, methods, allow_headers, expose_headers, max_age
            )

            rv = f(*args, **kwargs)
            add_responder(responder)
            return rv

        return crossdomain_inner_fn

    return decorator
