from unittest import TestCase

from injector import Module, singleton

from zsl import inject
from zsl.application.containers.core_container import CoreContainer
from zsl.interface.task_queue import TaskQueueWorker, run_worker
from zsl.testing.db import IN_MEMORY_DB_SETTINGS
from zsl.testing.zsl import ZslTestCase, ZslTestConfiguration


class DummyWorker(TaskQueueWorker):

    def __init__(self):
        super(DummyWorker, self).__init__()
        self.run_count = 0

    def run(self):
        self.run_count += 1

    def stop_worker(self):
        pass


class DummyWorkerTaskQueueModule(Module):

    def configure(self, binder):
        worker = DummyWorker()
        binder.bind(TaskQueueWorker, to=worker, scope=singleton)


class DummyWorkerContainer(CoreContainer):
    dummy_worker = DummyWorkerTaskQueueModule


class RunDummyWorkerWithoutParamsTestCase(ZslTestCase, TestCase):
    CONFIG = IN_MEMORY_DB_SETTINGS.copy()
    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        app_name='RunDummyWorkerWithoutParamsTestCase', container=DummyWorkerContainer,
        config_object=CONFIG)

    @inject(worker=TaskQueueWorker)
    def testWorkerRunCount(self, worker):
        self.assertEqual(worker.run_count, 0, "worker.run() shouldn't be called yet.")

        run_worker()

        self.assertEqual(worker.run_count, 1, "worker.run() should be called exactly once.")
