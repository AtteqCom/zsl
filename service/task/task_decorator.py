'''
Created on 12.12.2012

@author: Martin Babka
'''
import json
from flask import request
from application.service_application import service_application
from task.task_data import TaskData

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

            if request.headers.get("Content-Type") != "application/json" and task_data != None:
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
            return json.dumps(ret_val)

        return wrapped_fn

def json_output(f):
    return JsonOutputDecorator()(f)

