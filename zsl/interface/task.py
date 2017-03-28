"""
:mod:`zsl.interface.task`
-------------------------

.. moduleauthor:: Peter Morihladko
"""
from __future__ import unicode_literals
from future.builtins import str

import json

from zsl import inject, Injected
from zsl.router.task import TaskRouter
from zsl.task.job_context import JobContext, Job


@inject(task_router=TaskRouter)
def exec_task(task_path, data, task_router=Injected):
    """Execute task.

    :param task_path: task path
    :type task_path: str
    :param data: task's data
    :type data: Any
    :param task_router: task router, injected
    :type task_router: TaskRouter
    :return:
    """
    if not data:
        data = {'data': None, 'path': task_path}

    elif not isinstance(data, (str, bytes)):
        data = json.dumps(data)

    # Open the data from file, if necessary.
    elif data is not None and data.startswith("file://"):
        with open(data[len("file://"):]) as f:
            data = f.read()

    # Prepare the task.
    job = Job(data)
    (task_, task_callable) = task_router.route(task_path)
    jc = JobContext(job, task_, task_callable)
    JobContext.set_current_context(jc)

    # Run the task.
    return jc.task_callable(jc.task_data)
