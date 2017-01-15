"""
:mod:`zsl.utils.task_helper`
----------------------------

Helper module for task management.

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals
from zsl.application.service_application import service_application
from zsl.task.task_data import TaskData

_app = service_application

TASK_PERFORM_METHOD = "perform"


def run_task(task_cls, task_data):
    """Instantiate and run the perform method od given task data.

    :param task_cls: task class
    :param task_data: task data
    :type task_data: TaskData
    :return: task's result
    """
    task = instantiate(task_cls)
    task_callable = get_callable(task)
    return task_callable(TaskData(_app, task_data))


def run_task_json(task_cls, task_data):
    """Instantiate and run the perform method od given task data.

    :param task_cls: task class
    :param task_data: task data
    :type task_data: TaskData
    :return: task's result
    """
    # TODO what does set_skipping_json do?
    task = instantiate(task_cls)
    task_callable = get_callable(task)
    td = TaskData(_app, task_data)
    td.set_skipping_json(True)
    return task_callable(td)


def get_callable(task):
    """Return the perform method on given task.

    :param task: task instance
    :return: bound perform method
    """
    return getattr(task, TASK_PERFORM_METHOD)


from zsl.utils.injection_helper import instantiate
