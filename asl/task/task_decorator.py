'''
Created on 12.12.2012

@author: Martin Babka
'''
import json
from flask import request
from asl.application.service_application import service_application
from asl.task.task_data import TaskData
from asl.db.model import AppModelJSONEncoder

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

            if task_data.get_data() != "":
                try:
                    # We transform the data only in the case of plain POST requests.
                    if request.headers.get("Content-Type") != "application/json" and task_data != None and not task_data.is_skipping_json():
                        task_data.transform_data(json.loads)
                except:
                    # app.logger.error("Exception while processing JSON input decorator.")
                    task_data.transform_data(json.loads)

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
                return json.dumps(ret_val, cls = AppModelJSONEncoder)
            else:
                return ret_val

        return wrapped_fn

def json_output(f):
    return JsonOutputDecorator()(f)

class ErrorAndResultDecorator:
    def __call__(self, fn):
        def wrapped_fn(*args):
            try:
                ret_val = fn(*args)

                return {
                    'data': ret_val
                }
            except Exception as e:
                return {
                    'error': e.to_string()
                }

        return wrapped_fn

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
            task_data = get_data(args)
            for i in self.data:
                if not i in task_data:
                    raise KeyError(i)

            return fn(*args)

def required_data(*data):
    return RequiredDataDecorator(data)
