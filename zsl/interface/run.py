#!/usr/bin/python
"""
:mod:`zsl.interface.run`
------------------------

.. moduleauthor:: Peter Morihladko <peter@atteq.com>, Martin Babka <babka@atteq.com>
"""
from __future__ import print_function
from __future__ import unicode_literals

from builtins import object


# Initialize the path
import sys
import click

# Initialize
from zsl.interface.importer import initialize_web_application

initialize_web_application()

import json
from zsl import Config
from zsl.utils.injection_helper import inject
from zsl.router import task_router
from zsl.interface.task_queue import Worker
from zsl.task.job_context import JobContext
from zsl.application import service_application

conf = service_application.config


class Job(object):
    def __init__(self, data):
        self.data = {'data': data}


@click.group()
def run():
    pass


@run.command()
def web():
    service_application.run(
        host=conf.get('FLASK_HOST', '127.0.0.1'),
        port=conf.get('FLASK_PORT'),
        debug=conf.get('DEBUG', False),
        use_debugger=conf.get('USE_DEBUGGER', False),
        use_reloader=conf.get('USE_RELOADER', False)
    )


@run.command()
def shell():
    import bpython

    bpython.embed()


@run.command()
@click.argument('task')
@click.argument('data', default=None, required=False)
def task(task, data=None):
    """
    .. autofunction:: run_task
    Runs the given task

    ..param:
    """
    if not isinstance(data, (str, bytes)):
        data = json.dumps(data)
    # Open the data from file, if necessary.
    elif data is not None and data.startswith("file://"):
        with open(data[len("file://"):]) as f:
            data = f.read()

    # Prepare the task.
    job = Job(data)
    (task, task_callable) = task_router.route(task)
    jc = JobContext(job, task, task_callable)
    JobContext.set_current_context(jc)

    # Run the task.
    return jc.task_callable(jc.task_data)


def run_celery_worker(argv):
    """

    :param argv: arguments for celery worker
    """
    from zsl.interface.celery.worker import CeleryWorker

    worker = CeleryWorker()
    worker.run(argv)


def run_gearman_worker():
    from zsl.interface.gearman.run_worker import main

    main()


@run.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('task_queue', type=click.Choice(['celery', 'gearman']))
@click.argument('argv', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def worker(ctx, task_queue, argv):
    if task_queue == 'celery':
        run_celery_worker(argv)
    elif task_queue == 'gearman':
        run_gearman_worker()


# Run it!
if __name__ == "__main__":
    run()
