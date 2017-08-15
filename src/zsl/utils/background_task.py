"""
:mod:`zsl.utils.background_task`
--------------------------------
"""
from __future__ import unicode_literals

from functools import wraps
from typing import Callable

from zsl_client import GearmanService, JsonTask, RawTask

from zsl import Config, inject
from zsl.utils.params_helper import required_params

__author__ = 'Peter Morihladko'


def background_task_method(task):
    """Decorate an object method as a background task (called with help of
    gearman).

    You have to create a task which will handle the gearman call. The
    method arguments will be encoded as JSON.

    :param task: name of the task
    :type task: str
    :return: decorated function
    """

    # TODO ako vysledok vrat nejaky JOB ID, aby sa dalo checkovat na pozadi
    # TODO vytvorit este vseobecny background_task nielen pre metody

    def decorator_fn(fn):

        gearman = None

        @inject(config=Config)
        def gearman_connect(config):
            # type: (Config) -> GearmanService
            if 'GEARMAN' not in config or 'host' not in config['GEARMAN'] or 'GEARMAN_TASK_NAME' not in config:
                raise Exception("Missing gearman settings (trying to use backgorund task)")

            gearman_host = (config['GEARMAN']['host'], config['GEARMAN']['port']) if config['GEARMAN']['port'] \
                else config['GEARMAN']['host']
            gearman_service = GearmanService({'HOST': [gearman_host], 'TASK_NAME': config['GEARMAN_TASK_NAME']})
            gearman_service.set_blocking(False)

            return gearman_service

        def get_gearman_client():
            # type: () -> GearmanService
            global gearman

            if not gearman:
                gearman = gearman_connect()

            return gearman

        @wraps(fn)
        def background_task_decorator(*args, **kwargs):
            # The first of the args is self.
            t = RawTask(task, dict(method=fn.__name__, args=args[1:], kwargs=kwargs))
            t_result = get_gearman_client().call(t, [JsonTask])
            return t_result.result

        background_task_decorator._background_fn = fn
        return background_task_decorator

    return decorator_fn


def get_background_method(obj, params):
    required_params(params, 'method', 'args', 'kwargs')

    method_name = params['method']
    args = params['args']
    kwargs = params['kwargs']

    method = getattr(obj, method_name)

    if not callable(method) or not hasattr(method, '_background_fn'):
        raise Exception('{0} is not a background task'.format(params['method']))

    method = getattr(method, '_background_fn')

    def original_fn():
        return method.__get__(obj, obj.__class__)(*args, **kwargs)

    return original_fn
