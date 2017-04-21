#!/usr/bin/python
"""
:mod:`zsl.interface.run`
------------------------

.. moduleauthor:: Peter Morihladko <peter@atteq.com>, Martin Babka <babka@atteq.com>
"""
from __future__ import print_function
from __future__ import unicode_literals

import json
import click
click.disable_unicode_literals_warning = True


from zsl import Zsl
from zsl.task.job_context import JobContext, Job

from zsl.application.containers.web_container import WebContainer
from zsl.application.containers.celery_container import CeleryContainer
from zsl.router.task import TaskRouter


@click.group()
def run():
    pass


@run.command()
def web():
    app = Zsl(__name__, modules=WebContainer.modules())

    app.run_web(
        host=app.config.get('FLASK_HOST', '127.0.0.1'),
        port=app.config.get('FLASK_PORT', 3000),
        debug=app.config.get('DEBUG', False),
        use_debugger=app.config.get('USE_DEBUGGER', False),
        use_reloader=app.config.get('USE_RELOADER', False)
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
    .. autofunction:: task
    Runs the given task

    ..param:
    """
    app = Zsl(__name__)

    if not data:
        data = {'data': None, 'path': task}
    elif not isinstance(data, (str, bytes)):
        data = json.dumps(data)
    # Open the data from file, if necessary.
    elif data is not None and data.startswith("file://"):
        with open(data[len("file://"):]) as f:
            data = f.read()

    task_router = app.injector.get(TaskRouter)

    # Prepare the task.
    job = Job(data)
    (task, task_callable) = task_router.route(task)
    jc = JobContext(job, task, task_callable)
    JobContext.set_current_context(jc)

    # Run the task.
    click.echo(jc.task_callable(jc.task_data))


def run_celery_worker(worker_args):
    """Ru Zsl celery worker.

    :param worker_args: arguments for celery worker
    """

    app = Zsl(__name__, modules=CeleryContainer.modules())

    app.run_worker(worker_args)


def run_gearman_worker():
    from zsl.interface.gearman.run_worker import main

    main()


@run.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('task_queue', type=click.Choice(['celery', 'gearman']))
@click.argument('argv', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def worker(_, task_queue, argv):
    if task_queue == 'celery':
        run_celery_worker(argv)
    elif task_queue == 'gearman':
        run_gearman_worker()


# Run it!
if __name__ == "__main__":
    run()
