'''
Created on 22.1.2013

@author: Martin Babka
'''
from asl.application.service_application import service_application
from asl.task.task_data import TaskData

_app = service_application

def run_task(task_cls, task_data):
    task = instantiate(task_cls)
    task_callable = get_callable(task)
    return task_callable(TaskData(_app, task_data))

def run_task_json(task_cls, task_data):
    task = instantiate(task_cls)
    task_callable = get_callable(task)
    td = TaskData(_app, task_data)
    td.set_skipping_json(True)
    return task_callable(td)

def get_callable(task):
    return getattr(task, "perform")

def instantiate(cls):
    injector = _app.get_injector()

    if hasattr(cls, "__new__"):
        task = injector.create_object(cls)
    else:
        task = cls()

    return task
