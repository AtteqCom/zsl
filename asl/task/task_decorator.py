'''
:mod:`asl.task.task_decorator`

.. moduleauthor:: Martin Babka
'''

import json
from flask import request
from asl.application.service_application import service_application
from asl.task.task_data import TaskData
from asl.db.model import AppModelJSONEncoder
from asl.task.job_context import JobContext, WebJobContext, Responder
import traceback
import hashlib
from functools import wraps
from asl.cache.id_helper import IdHelper
from os.path import os
import errno


def log_output(f):
    '''
    Logs the output value.
    '''

    @wraps(f)
    def wrapper_fn(*args, **kwargs):
        res = f(*args, **kwargs)
        service_application.logger.debug("Logging result %s.", res)
        return res

    return wrapper_fn

def save_to_file(dst):
    '''
    Save the output value to file.
    '''

    dst = dst

    def decorator_fn(f):

        @wraps(f)
        def wrapper_fn(*args, **kwargs):
            res = f(*args, **kwargs)

            try:
                os.makedirs(os.path.dirname(dst))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            with open(dst, "w") as text_file:
                text_file.write(res)

            return res

        return wrapper_fn
    return decorator_fn

def json_input(f):
    '''
    Expects task input data in json format and parse this data.
    '''

    @wraps(f)
    def json_input_decorator(*args, **kwargs):
        # If the data is already transformed, we do not transform it any further.
        task_data = get_data(args)

        if task_data == None:
            app.logger.error("Task data is empty during JSON decoding.")

        if task_data.get_data():
            try:
                # We transform the data only in the case of plain POST requests.
                if not request.json and task_data != None and not task_data.is_skipping_json():
                    task_data.transform_data(json.loads)
            except:
                # app.logger.error("Exception while processing JSON input decorator.")
                task_data.transform_data(json.loads)
        else:
            task_data.transform_data(lambda _: {})

        return f(*args, **kwargs)

    return json_input_decorator


def json_output(f):
    '''
    Format response to json and in case of web-request set response content-type to 'application/json'.
    '''

    @wraps(f)
    def json_output_decorator(*args, **kwargs):
        rv = f(*args, **kwargs)

        skip_encode = False
        for d in args:
            if isinstance(d, TaskData):
                skip_encode = d.is_skipping_json()

        if not skip_encode:
            rv = json.dumps(rv, cls = AppModelJSONEncoder)
            if isinstance(JobContext.get_current_context(), WebJobContext):
                JobContext.get_current_context().add_responder(MimeSetterWebTaskResponder('application/json'))

        return rv

    return json_output_decorator

def jsonp_wrap(callback_key = 'callback'):
    '''
    Format response to jsonp and add a callback to JSON data - a jsonp request
    '''
    callback_key = callback_key

    def decorator_fn(f):

        @wraps(f)
        def jsonp_output_decorator(*args, **kwargs):
            task_data = get_data(args)
            data = task_data.get_data()

            if not callback_key in data:
                raise KeyError('Missing required parameter "{0}" for task.'.format(callback_key))

            callback = data[callback_key]
            jsonp = f(*args, **kwargs)
            if isinstance(JobContext.get_current_context(), WebJobContext):
                JobContext.get_current_context().add_responder(MimeSetterWebTaskResponder('application/javascript'))
            jsonp = "{callback}({data})".format(callback=callback, data=jsonp)

            return jsonp

        return jsonp_output_decorator

    return decorator_fn

def jsend_output(fail_exception_classes = None):
    '''
    Format task result to json output in jsend specification format. See: http://labs.omniti.com/labs/jsend.
    Task return value must be dict or None.

    @param fail_exception_classes: exceptions which will produce 'fail' response status
    '''

    fail_exception_classes = fail_exception_classes if fail_exception_classes else ()

    def decorator_fn(f):

        @wraps(f)
        @json_output
        def jsend_output_decorator(*args, **kwargs):
            try:
                rv = f(*args, **kwargs)
            except fail_exception_classes as e:
                return {'status': 'fail', 'data': {'message': unicode(e)}}
            except Exception as e:
                service_application.logger.error(unicode(e) + "\n" + traceback.format_exc())
                return {'status': 'error', 'message': 'Server error.'}

            if not isinstance(rv, dict) and rv is not None:
                msg = 'jsend_output decorator error: task must return dict or None.'
                service_application.logger.error(msg + '\ntask return value: {0}'.format(rv))
                return {'status': 'error', 'message': 'Server error.'}

            return {'status': 'success', 'data': rv}

        return jsend_output_decorator

    return decorator_fn

def web_error_and_result(f):
    '''
    Same as error_and_result decorator, except:
    If no exception was raised during task execution, ONLY IN CASE OF WEB REQUEST formats
    task result into json dictionary {'data': task return value}
    '''

    @wraps(f)
    def web_error_and_result_decorator(*args, **kwargs):
        return error_and_result_decorator_inner_fn(f, True, *args, **kwargs)

    return web_error_and_result_decorator

def error_and_result(f):
    '''
    Format task result into json dictionary {'data': task return value} if no exception was raised during task execution.
    If there was raised an exception during task execution, formats task result into dictionary {'error': exception message with traceback}
    '''

    @wraps(f)
    def error_and_result_decorator(*args, **kwargs):
        return error_and_result_decorator_inner_fn(f, False, *args, **kwargs)

    return error_and_result_decorator


def required_data(*data):
    '''
    Task decorator which checks if the given variables (indices) are stored inside the task data.
    '''

    def decorator_fn(f):

        @wraps(f)
        def required_data_decorator(*args, **kwargs):
            task_data = get_data(args).get_data()
            for i in data:
                if not i in task_data:
                    raise KeyError('Missing required parameter "{0}" for task.'.format(i))

            return f(*args, **kwargs)

        return required_data_decorator

    return decorator_fn

def append_get_parameters(accept_only_web = True):
    '''
    Task decorator which appends the GET data to the task data.

    :param boolean accept_only_web: Parameter which limits using this task only with web requests.
    '''

    def wrapper(f):
        @wraps(f)
        def append_get_parameters(*args, **kwargs):
            jc = JobContext.get_current_context()

            if isinstance(jc, WebJobContext):
                # Update the data with GET parameters
                request = jc.get_web_request()
                task_data = get_data(args)
                data = task_data.get_data()
                data.update(request.args.to_dict(flat=True))
            elif accept_only_web:
                # Raise exception on non web usage if necessary
                raise Exception("append_get_parameters decorator may be used with GET requests only.")


            return f(*args, **kwargs)

        return append_get_parameters

    return wrapper

def web_task(f):
    '''
    Checks if the task is called through the web interface.
    Task return value should be in format {'data': ...}.
    '''

    @wraps(f)
    def web_task_decorator(*args, **kwargs):
        jc = JobContext.get_current_context()
        if not isinstance(jc, WebJobContext):
            raise Exception("The WebTask is not called through the web interface.")
        data = f(*args, **kwargs)
        jc.add_responder(WebTaskResponder(data))
        return data['data'] if 'data' in data else ""

    return web_task_decorator


def secured_task(f):
    '''
    Secured task decorator.
    '''

    secure_token = service_application.config['SERVICE_SECURITY_TOKEN']

    def compute_token(random_token):
        sha1hash = hashlib.sha1()
        sha1hash.update(random_token + secure_token)
        return sha1hash.hexdigest().upper()

    @wraps(f)
    def secured_task_decorator(*args, **kwargs):
        task_data = get_data(args)
        assert isinstance(task_data, TaskData)
        random_token = task_data.get_data()['security']['random_token']
        hashed_token = task_data.get_data()['security']['hashed_token']
        task_data.transform_data(lambda x: x['data'])
        if unicode(hashed_token) != unicode(compute_token(random_token)):
            raise SecurityException(hashed_token)

        return f(*args, **kwargs)

    return secured_task_decorator

def xml_output(f):
    '''
    Set content-type for response to WEB-REQUEST to 'text/xml'
    '''

    @wraps(f)
    def xml_output(*args, **kwargs):
        retval = f(*args, **kwargs)

        if isinstance(JobContext.get_current_context(), WebJobContext):
            JobContext.get_current_context().add_responder(MimeSetterWebTaskResponder('text/xml'))
        return retval

    return xml_output

def file_upload(f):
    '''
    Return list of werkzeug.datastructures.FileStorage objects - files to be uploaded
    TODO: maybe delete
    '''

    @wraps(f)
    def file_upload_decorator(*args, **kwargs):
        # If the data is already transformed, we do not transform it any further.
        task_data = get_data(args)

        if task_data == None:
            app.logger.error("Task data is empty during FilesUploadDecorator.")

        task_data.transform_data(lambda _: request.files.getlist('file'))

        return f(*args, **kwargs)

    return file_upload_decorator

# TODO toto je len quick and dirty riesenie
def cache_json_output(key, timeout):
    cache = get_id_helper()

    def wrapper_fn(f):

        @wraps(f)
        def cache_simple_output_decorator(*args, **kwargs):
            rv = cache.get_key(key)

            if rv:
                try:
                    rv = json.loads(rv)
                except ValueError:
                    rv = None

            if not rv:
                rv = f(*args, **kwargs)
                cache.set_key(key, json.dumps(rv), timeout)

            return rv

        return cache_simple_output_decorator

    return wrapper_fn


###############
### helpers ###
###############

app = service_application

def get_data(a):
    task_data = None
    for d in a:
        if isinstance(d, TaskData):
            task_data = d

    return task_data

class SecurityException(Exception):

    def __init__(self, hashed_token):
        Exception.__init__(self, "Invalid hashed token '{0}'.".format(hashed_token))
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

def error_and_result_decorator_inner_fn(f, web_only, *args, **kwargs):
    try:
        ret_val = f(*args, **kwargs)
        if web_only and not isinstance(JobContext.get_current_context(), WebJobContext):
            rv = ret_val
        else:
            rv = {'data': ret_val}

    except Exception:
        exc = traceback.format_exc()
        app.logger.error(exc)
        rv = {'error': "{0}".format(exc)}

    return json.dumps(rv)

def get_id_helper():
    return app.get_injector().get(IdHelper)
