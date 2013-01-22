'''
Created on 22.1.2013

@author: Martin Babka
'''
from application.service_application import service_application
from task.task_data import TaskData

class TaskHelper:

    __app = service_application

    @classmethod
    def run_task(self_cls, task_cls, task_data):
        task = TaskHelper.instantiate(task_cls)
        task_callable = TaskHelper.get_callable(task)
        return task_callable(TaskData(self_cls.__app, task_data))

    @classmethod
    def run_task_json(self_cls, task_cls, task_data):
        task = TaskHelper.instantiate(task_cls)
        task_callable = TaskHelper.get_callable(task)
        td = TaskData(self_cls.__app, task_data)
        td.set_skipping_json(True)
        return task_callable(td)

    @staticmethod
    def get_callable(task):
        return getattr(task, "perform")

    @classmethod
    def instantiate(self_cls, cls):
        injector = self_cls.__app.get_injector()

        if hasattr(cls, "__new__"):
            task = injector.create_object(cls)
        else:
            task = cls()

        return task