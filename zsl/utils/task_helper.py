'''
:mod:`asl.utils.task_helper`

.. moduleauthor:: Martin Babka
'''
from zsl.application.service_application import service_application
from zsl.task.task_data import TaskData

_app = service_application

TASK_PERFORM_METHOD = "perform"

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
    return getattr(task, TASK_PERFORM_METHOD)

from injection_helper import instantiate

