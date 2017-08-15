"""
:mod:`zsl.application.modules.celery_module`
--------------------------------------------
"""
from __future__ import unicode_literals

import click
from injector import Module, singleton

from zsl import Injected, Zsl
from zsl.application.modules.cli_module import ZslCli
from zsl.interface.celery.worker import (CeleryTaskQueueMainWorker, CeleryTaskQueueOutsideWorker,
                                         CeleryTaskQueueWorkerBase)
from zsl.interface.task_queue import TaskQueueWorker, run_worker
from zsl.utils.injection_helper import inject, simple_bind


class CeleryTaskQueueMainWorkerModule(Module):
    """Adds celery worker to current configuration."""

    def configure(self, binder):
        worker = CeleryTaskQueueMainWorker()
        binder.bind(TaskQueueWorker, to=worker, scope=singleton)
        binder.bind(CeleryTaskQueueWorkerBase, to=worker, scope=singleton)


class CeleryTaskQueueOutsideWorkerModule(Module):
    """Adds celery outside worker to current configuration.

    Outside worker is meant to run with help of celery cli tools.
    """

    def configure(self, binder):
        worker = CeleryTaskQueueOutsideWorker()
        binder.bind(TaskQueueWorker, to=worker, scope=singleton)
        binder.bind(CeleryTaskQueueWorkerBase, to=worker, scope=singleton)


class CeleryCli(object):
    @inject(zsl_cli=ZslCli)
    def __init__(self, zsl_cli):
        # type: (ZslCli) ->  CeleryCli

        @zsl_cli.cli.group(help='Celery related tasks.')
        def celery():
            pass

        @celery.command(help="run worker",
                        context_settings=dict(ignore_unknown_options=True))
        @click.argument('argv', nargs=-1, type=click.UNPROCESSED)
        @click.pass_context
        def worker(_, argv):
            """Run Zsl celery worker.

            :param : arguments for celery worker
            """
            run_worker(argv)

        self._celery = celery

    def celery(self):
        return self._celery


class CeleryCliModule(Module):
    def configure(self, binder):
        simple_bind(binder, CeleryCli, singleton)
