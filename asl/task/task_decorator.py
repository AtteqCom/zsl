'''
Created on 12.12.2012

@author: Martin Babka
'''
import json
from flask import request
from asl.application.service_application import service_application
from asl.task.task_data import TaskData
from asl.db.models.app import AppModelJSONEncoder

app = service_application

class CompundTask:
    def __init__(self):
        pass

    def __call__(self, fn):
        def wrapped_fn(*args):
            return fn(*args)

        return wrapped_fn

def compound_task(*a):
    return CompundTask(*a)

class IdCacheVerifier:
    def __init__(self):
        pass

    def __call__(self, fn):
        def wrapped_fn(*args):
            return fn(*args)

        return wrapped_fn

def id_cache_verifier(*a):
    return IdCacheVerifier(*a)

class JsonInput:
    def __init__(self):
        pass

    def __call__(self, fn):
        def wrapped_fn(*a):
            # If the data is already transformed, we do not transform it any further.
            task_data = None
            for d in a:
                if isinstance(d, TaskData):
                    task_data = d

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
    def __init__(self):
        pass

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

