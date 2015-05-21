'''
:mod:`client.python.asl.client` -- ASL python client module
===========================================================

Python client which allows to connect to web and gearman service and delivers tasks to them.
For usage of this module just use `import asl.client` and add the path `client/python` to `PYTHON_PATH`.

   :platform: Unix, Windows
   :synopsis: The Atteq Service Layer python client.
.. moduleauthor:: Martin Babka <babka@atteq.com>
'''
from abc import abstractmethod

import hashlib
import json
import random
import urllib2

import gearman

def _random_string(length, allowed_characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'):
    return ''.join(random.choice(allowed_characters) for _ in range(length))

class Task:
    @abstractmethod
    def get_name(self):
        pass
    name = property(get_name)

    @abstractmethod
    def get_data(self):
        pass
    data = property(get_data)

class RawTask(Task):
    def __init__(self, name, data):
        self._name = name
        self._data = data

    def get_name(self):
        return self._name
    name = property(get_name)

    def get_data(self):
        return self._data
    data = property(get_data)

class TaskResult:
    @abstractmethod
    def get_task(self):
        pass
    task = property(get_task)

    @abstractmethod
    def get_result(self):
        pass
    result = property(get_result)

class RawTaskResult(TaskResult):
    def __init__(self, task, result):
        assert isinstance(task, Task)
        self._task = task
        self._result = result

    def get_task(self):
        return self._task

    def get_result(self):
        return self._result

class TaskDecorator(Task):
    def __init__(self, task):
        self._task = task

    def get_name(self):
        return self._task.get_name()

    def get_data(self):
        return self._task.get_data()

class JsonTask(Task, TaskDecorator):
    def get_name(self):
        return TaskDecorator.get_name(self)

    def get_data(self):
        data = self._task.get_data()
        return json.dumps(data)

class SecuredTask(Task, TaskDecorator):
    def get_name(self):
        return TaskDecorator.get_name(self)

    def set_asl(self, asl):
        self._asl = asl

    def get_data(self):
        random_token = _random_string(16)
        return {
            "data": self._task.get_data(),
            "security": {
                "random_token": random_token,
                "hashed_token": hashlib.sha1(random_token + self._asl.get_secure_token()).hexdigest().upper()
            }
        }

class TaskResultDecorator:
    def __init__(self, task_result):
        assert isinstance(task_result, TaskResult)
        self._task_result = task_result

class JsonTaskResult(TaskResult, TaskResultDecorator):
    def get_result(self):
        result = self._task_result.get_result()
        return json.loads(result)

class ErrorTaskResult(TaskResult, TaskResultDecorator):
    def get_complete_result(self):
        result = self._task_result.get_result()
        return result

    def get_result(self):
        result = self._task_result.get_result()
        return json.loads(result['data'])

    def is_error(self):
        result = self._task_result.get_result()
        return True if 'error'in result else False

    def get_error(self):
        return self._task_result.get_result()['error']

class Service:
    @abstractmethod
    def _inner_call(self, name, data):
        '''
        Make request to service layer and returns response to this request.

        :param name: name of the task
        :type name: str
        :param data: task data

        :return response to task request on service layer
        '''
        pass

    def call(self, task, decorators = []):
        '''
        Call given task on service layer.

        :param task: task to be called. task will be decorated with
            TaskDecorator's contained in 'decorators' list
        :type task: instance of Task class
        :param decorators: list of TaskDecorator's / TaskResultDecorator's
            inherited classes
        :type decorators: list

        :return task_result: result of task call decorated with TaskResultDecorator's
            contained in 'decorators' list
        :type task_result: TaskResult instance
        '''
        task = self.apply_task_decorators(task, decorators)

        data = task.get_data()
        name = task.get_name()

        result = self._inner_call(name, data)
        task_result = RawTaskResult(task, result)
        return self.apply_task_result_decorators(task_result, decorators)

    def apply_task_decorators(self, task, decorators):
        for d in decorators:
            if TaskDecorator in d.__bases__:
                task = d(task)
                if hasattr(task, 'set_asl'):
                    task.set_asl(self)

        return task

    def apply_task_result_decorators(self, task_result, decorators):
        for d in decorators:
            if TaskResultDecorator in d.__bases__:
                task_result = d(task_result)

        return task_result

    def get_secure_token(self):
        return self._security_config['SECURITY_TOKEN']

class GearmanService(Service):
    def __init__(self, gearman_config, security_config=None):
        self._gearman_config = gearman_config
        self._security_config = security_config
        self._gearman_client = gearman.client.GearmanClient(self._gearman_config['HOST'])
        self._blocking_status = True

    def set_blocking(self, blocking_status):
        self._blocking_status = blocking_status

    def _inner_call(self, name, data):
        if data is None:
            data = "null"
        elif not (isinstance(data, unicode) or isinstance(data, str)):
            data = str(data)

        completed_job_request = self._gearman_client.submit_job(
            self._gearman_config['TASK_NAME'],
            json.dumps({
                'path': name,
                'data': data
            }),
            background = not self._blocking_status
        )

        if self._blocking_status:
            return completed_job_request.result

class WebService(Service):
    def __init__(self, web_config, security_config):
        self._web_config = web_config
        self._security_config = security_config
        self._service_layer_url = self._web_config['SERVICE_LAYER_URL']

    def get_service_layer_url(self):
        return self._service_layer_url

    def _inner_call(self, name, data):
        if data is None:
            data = "null"
        elif not (isinstance(data, unicode) or isinstance(data, str)):
            data = str(data)

        req = urllib2.Request(self._service_layer_url + name, data, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        returned_data = f.read()
        f.close()
        return returned_data
