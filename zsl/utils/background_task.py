from client.python.asl.client import GearmanService, RawTask, JsonTask
from zsl.application.service_application import service_application as app
from functools import wraps
from zsl.utils.params_helper import required_params

__author__ = 'Peter Morihladko'


def background_task_method(task):
    """
    Decorate an object method as a background task (called with help of
    gearman)

    You have to create a task which will handle the gearman call. The
    method arguments will be encoded as JSON.

    :param task: name of the task
    :type task: str
    :return: decorated function
    """

    # TODO ako vysledok vrat nejaky JOB ID, aby sa dalo checkovat na pozadi
    # TODO vytvorit este vseobecny background_task nielen pre metody

    def decorator_fn(fn):
        if 'GEARMAN' not in app.config or 'host' not in app.config['GEARMAN'] or 'GEARMAN_TASK_NAME' not in app.config:
            raise Exception("Missing gearman settings (trying to use backgorund task)")

        gearman_host = (app.config['GEARMAN']['host'], app.config['GEARMAN']['port']) if app.config['GEARMAN']['port'] \
            else app.config['GEARMAN']['host']
        gearman = GearmanService({'HOST': [gearman_host], 'TASK_NAME': app.config['GEARMAN_TASK_NAME']})
        gearman.set_blocking(False)

        @wraps(fn)
        def background_task_decorator(*args, **kwargs):
            # The first of the args is self.
            t = RawTask(task, dict(method=fn.__name__, args=args[1:], kwargs=kwargs))
            t_result = gearman.call(t, [JsonTask])
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
