'''
Created on 12.12.2012

@author: Martin Babka
'''

import json
from flask import request
from asl.application.service_application import service_application
from asl.task.task_data import TaskData
from asl.db.model import AppModelJSONEncoder
from asl.task.job_context import JobContext, WebJobContext, Responder
import traceback
import hashlib
from asl.db.model.app_model import AppModel

app = service_application

def get_data(a):
    task_data = None
    for d in a:
        if isinstance(d, TaskData):
            task_data = d

    return task_data

class JsonInput:
    def __call__(self, fn):
        def wrapped_fn(*a):
            # If the data is already transformed, we do not transform it any further.
            task_data = get_data(a)

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

            return fn(*a)

        return wrapped_fn

def json_input(f):
    return JsonInput()(f)

class JsonOutputDecorator:
    def __call__(self, fn):
        def wrapped_fn(*args):
            ret_val = fn(*args)

            skip_encode = False
            for d in args:
                if isinstance(d, TaskData):
                    skip_encode = d.is_skipping_json()

            if not skip_encode:
                ret_val = json.dumps(ret_val, cls = AppModelJSONEncoder)
                if isinstance(JobContext.get_current_context(), WebJobContext):
                    JobContext.get_current_context().add_responder(MimeSetterWebTaskResponder('application/json'))

            return ret_val

        return wrapped_fn

def json_output(f):
    return JsonOutputDecorator()(f)

class JsendOutputDecorator:
    def __init__(self, fail_exception_classes):
        if fail_exception_classes is None:
            self._fail_exception_classes = ()
        else:
            self._fail_exception_classes = fail_exception_classes

    def __call__(self, fn):
        
        @json_output
        def wrapped_fn(*args):
            try:
                ret_val = fn(*args)
            except self._fail_exception_classes as e:
                return {'status': 'fail', 'data': {'message': unicode(e)}}
            except Exception as e:
                service_application.logger.error(unicode(e) + "\n" + traceback.format_exc())
                return {'status': 'error', 'message': 'Server error.'}

            # TODO najst lepsie riesenie, ako zistit, ci ret_val bude po JSON dumpe
            # JSON objekt alebo null alebo nieco ine
            if not isinstance(ret_val, AppModel) and not isinstance(ret_val, dict)\
                and ret_val is not None:
                msg = 'JsendOutputDecorator error: ' + \
                    'function return value is after JSON dump nor JSON object nor null.'
                service_application.logger.error(msg + '\nfunction return value: {0}'.format(ret_val))
                return {'status': 'error', 'message': msg}

            return {'status': 'success', 'data': ret_val}

        return wrapped_fn

def jsend_output(fail_exception_classes = None):
    def decorator_fn(f):
        return JsendOutputDecorator(fail_exception_classes)(f)
    
    return decorator_fn


class ErrorAndResultDecorator:
    def __init__(self, web_only = False):
        self._web_only = web_only

    def __call__(self, fn):
        def inner_wrapped_fn(*args):
            try:
                ret_val = fn(*args)
                if self._web_only and not isinstance(JobContext.get_current_context(), WebJobContext):
                    return ret_val

                return {
                    'data': ret_val
                }
            except Exception:
                exc = traceback.format_exc()
                app.logger.error(exc)
                return {
                    'error': "{0}".format(exc)
                }

        def wrapped_fn(*args):
            result = inner_wrapped_fn(*args)
            return json.dumps(result)

        return wrapped_fn

def web_error_and_result(f):
    return ErrorAndResultDecorator(True)(f)

def error_and_result(f):
    return ErrorAndResultDecorator()(f)

class RequiredDataDecorator:
    '''
    Task decorator which checks if the given variables (indices) are stored inside the task data.
    '''

    def __init__(self, data):
        self.data = data

    def __call__(self, fn):
        def wrapped_fn(*args):
            task_data = get_data(args).get_data()
            for i in self.data:
                if not i in task_data:
                    raise KeyError(i)

            return fn(*args)

        return wrapped_fn

def required_data(*data):
    return RequiredDataDecorator(data)

def append_get_parameters(f):
    '''
    Task decorator which appends the GET data to the task data.
    '''

    def append_get_parameters(*args, **kwargs):
        task_data = get_data(args)
        jc = JobContext.get_current_context()

        if not isinstance(jc, WebJobContext):
            raise Exception("AppendGetDataDecorator may be used with GET requests only.")

        request = jc.get_web_request()
        data = task_data.get_data()

        data.update(request.args.to_dict(flat=True))

        return f(*args, **kwargs)

    return append_get_parameters

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

class WebTaskDecorator:
    '''
    Checks if the task is called through the web interface.
    '''

    def __call__(self, fn):
        def wrapped_fn(*args):
            jc = JobContext.get_current_context()
            if not isinstance(jc, WebJobContext):
                raise Exception("The WebTask is not called through the web interface.")
            data = fn(*args)
            jc.add_responder(WebTaskResponder(data))
            return data['data'] if 'data' in data else ""

        return wrapped_fn

def web_task(f):
    return WebTaskDecorator()(f)


class SecurityException(Exception):

    def __init__(self, hashed_token):
        Exception.__init__(self, "Invalid hashed token '{0}'.".format(hashed_token))
        self._hashed_token = hashed_token

    def get_hashed_token(self):
        return self._hashed_token

class SecuredTaskDecorator:
    '''
    Checks if the task is called through the web interface.
    '''

    def __init__(self):
        self._secure_token = service_application.config['SERVICE_SECURITY_TOKEN']

    def __call__(self, fn):
        def wrapped_fn(*args):
            task_data = get_data(args)
            assert isinstance(task_data, TaskData)
            random_token = task_data.get_data()['security']['random_token']
            hashed_token = task_data.get_data()['security']['hashed_token']
            task_data.transform_data(lambda x: x['data'])
            if unicode(hashed_token) != unicode(self.compute_token(random_token)):
                raise SecurityException(hashed_token)

            return fn(*args)

        return wrapped_fn

    def compute_token(self, random_token):
        sha1hash = hashlib.sha1()
        sha1hash.update(random_token + self._secure_token)
        return sha1hash.hexdigest().upper()

def secured_task(f):
    return SecuredTaskDecorator()(f)

def xml_output(f):
    '''
    Create xml response for output
    '''
    def xml_output(*args, **kwargs):
        retval = f(*args, **kwargs)

        if isinstance(JobContext.get_current_context(), WebJobContext):
            JobContext.get_current_context().add_responder(MimeSetterWebTaskResponder('text/xml'))
        return retval

    return xml_output

class FileUploadDecorator:
    '''
    Return list of werkzeug.datastructures.FileStorage objects - files to be uploaded
    '''
    def __call__(self, fn):
        def wrapped_fn(*a):
            # If the data is already transformed, we do not transform it any further.
            task_data = get_data(a)

            if task_data == None:
                app.logger.error("Task data is empty during FilesUploadDecorator.")

            task_data.transform_data(lambda _: request.files.getlist('file'))

            return fn(*a)

        return wrapped_fn

def file_upload(f):
    return FileUploadDecorator()(f)

# TODO dopis
# def web_request(f):
#     '''
#     Create
#     '''
#
#     def web_request(*args, **kwargs):
#         ctx = JobContext.get_current_context()
#
#         if not isinstance(ctx, WebJobContext):
#             return
#
#         req = ctx.get_request() #_request
#
