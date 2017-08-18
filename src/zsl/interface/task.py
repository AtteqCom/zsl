"""
:mod:`zsl.interface.task`
-------------------------

.. moduleauthor:: Peter Morihladko <morihladko@atteq.com>,
                  Martin Babka <babka@atteq.com>
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *  # NOQA
from functools import wraps
import json
from json.encoder import JSONEncoder
import sys
from typing import Any, Callable, Dict

from future.builtins import str

from zsl import inject
from zsl.errors import ZslError
from zsl.router.task import TaskRouter
from zsl.task.job_context import Job, delegating_job_context
from zsl.task.task_data import TaskData
from zsl.utils.reflection_helper import is_scalar


class ModelConversionError(Exception):
    def __init__(self, obj, attribute):
        msg = "Can not fit dictionary into model '{0}' since the model does not have attribute '{1}'"
        super(ModelConversionError, self).__init__(msg.format(obj, attribute))
        self._obj = obj
        self._attribute = attribute

    @property
    def obj(self):
        return self._obj

    @property
    def attribute(self):
        return self._attribute


def fill_model_with_payload(data, obj):
    # type:(Dict[str, Any])->Any
    for k, v in data.items():
        if not hasattr(obj, k):
            raise ModelConversionError(obj, k)

        if is_scalar(v):
            setattr(obj, k, v)
        else:
            fill_model_with_payload(v, getattr(obj, k))


def payload_into_model(model_type, argument_name='request', remove_data=True):
    # type: (Callable, str)->Callable
    def wrapper(f):
        @wraps(f)
        def executor(*args, **kwargs):
            data = args[1]  # type: TaskData
            model = model_type()
            fill_model_with_payload(data.payload, model)
            kwargs[argument_name] = model
            if remove_data:
                args = args[:-1]
            return f(*args, **kwargs)

        return executor

    return wrapper


def create_simple_model(name, items, defaults=None, parent=object,
                        model_module=None):
    if defaults is None:
        defaults = {}
    default_code = "self.{0} = {0} if {0} is not None " \
                   "else (defaults.get('{0}', None))"
    item_definitions = "; ".join(map(lambda i: default_code.format(i), items))
    arglist = '=None, '.join(items) + ("=None, **kwargs" if len(items) else "**kwargs")
    class_code = """
class {name}(parent):
    def __new__(_cls, {arglist}):
        self = parent.__new__(_cls, **kwargs)
        {items}
        return self
    """.format(name=name, items=item_definitions, arglist=arglist)
    namespace = {'parent': parent, 'defaults': defaults}
    exec(class_code, namespace)
    result = namespace[name]
    result._source = class_code
    if model_module is None:
        try:
            model_module = sys._getframe(1).f_globals.get('__name__',
                                                          '__main__')
        except (AttributeError, ValueError):
            pass
    if model_module is not None:
        result.__module__ = model_module
    return result


class RequestJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, object):
            return dict(o.__dict__)
        else:
            return JSONEncoder.default(self, o)


def exec_task(task_path, data):
    """Execute task.

    :param task_path: task path
    :type task_path: str|Callable
    :param data: task's data
    :type data: Any
    :return:
    """
    if not data:
        data = {'data': None, 'path': task_path}

    elif not isinstance(data, (str, bytes)):
        data = {'data': json.dumps(data, cls=RequestJSONEncoder),
                'path': task_path}

    else:
        # Open the data from file, if necessary.
        if data is not None and data.startswith("file://"):
            with open(data[len("file://"):]) as f:
                data = f.read()

        data = {'data': data, 'path': task_path}

    # Prepare the task.
    job = Job(data)
    (task, task_callable) = create_task(task_path)

    with delegating_job_context(job, task, task_callable) as jc:
        return jc.task_callable(jc.task_data)


@inject(task_router=TaskRouter)
def create_task(task_path, task_router):
    if isinstance(task_path, str):
        (task, task_callable) = task_router.route(task_path)
    elif task_path is Callable or isinstance(task_path, type):
        task = task_path()
        task_callable = task.perform
    else:
        raise ZslError(
            "Can not create task with path '{0}'.".format(task_path))

    return task, task_callable
