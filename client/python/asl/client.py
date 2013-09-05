'''
Created on 9.8.2013

@author: Martin Babka
'''
from abc import abstractmethod
import json
import gearman

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

    def get_result(self, result):
        return self._result

class TaskDecorator:
    def __init__(self, task):
        self._task = task

class JsonTask(Task, TaskDecorator):
    def get_data(self):
        data = self._task.get_data(self)
        return json.dumps(data)

class SecuredTask(Task, TaskDecorator):
    def get_data(self):
        return {
            "data": self._task.data,
            "security": {
                "random_token": "",
                "hashed_token": ""
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

class Service:
    @abstractmethod
    def _inner_call(self, data):
        pass

    def call(self, task, decorators = []):
        task = self.apply_task_decorators(task, decorators)
        data = task.data
        name = task.name
        result = self._inner_call(name, data)
        task_result = RawTaskResult(task, result)
        return self.apply_task_result_decorators(task_result, decorators)

    def apply_task_decorators(self, task, decorators):
        for d in decorators:
            if TaskDecorator in d.__bases__:
                task = d(task)

        return task

    def apply_task_result_decorators(self, task_result, decorators):
        for d in decorators:
            if TaskResultDecorator in d.__bases__:
                task_result = d(task_result)

        return task_result

class GearmanService(Service):
    def __init__(self, gearman_config, security_config):
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
