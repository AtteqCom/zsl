"""
:mod:`zsl.application.modules.gearman_module`
---------------------------------------------
"""
from __future__ import unicode_literals

import click
from injector import Module, ClassProvider, singleton

from zsl import Zsl, inject
from zsl.application.modules.cli_module import ZslCli
from zsl.interface.gearman.task_filler import exec_task_filler
from zsl.interface.task_queue import TaskQueueWorker
from zsl.interface.gearman.worker import GearmanTaskQueueWorker
from zsl.utils.injection_helper import simple_bind


class GearmanCli(object):
    @inject(zsl_cli=ZslCli)
    def __init__(self, zsl_cli):
        # type: (ZslCli)->GearmanCli

        @zsl_cli.cli.group("Gearman related tasks.")
        def gearman():
            pass

        @gearman.command(help="run worker")
        @inject(zsl=Zsl)
        def worker(app):
            # type: (Zsl) -> None
            app.run_worker()

        @gearman.command()
        @click.argument('task_path', metavar='task')
        @click.argument('data', default=None, required=False)
        def task_filler(task_path, data):
            exec_task_filler(task_path, data)

        self._gearman = gearman

    @property
    def gearman(self):
        return self._gearman


class GearmanModule(Module):
    """Adds gearman to current configuration."""

    def configure(self, binder):
        binder.bind(TaskQueueWorker, to=ClassProvider(GearmanTaskQueueWorker), scope=singleton)
        simple_bind(binder, GearmanCli, singleton)
