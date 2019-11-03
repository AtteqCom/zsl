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
        self.last_param_1 = None
        self.last_param_2 = None

    def run(self, param_1, param_2='ahoj'):
        self.run_count += 1
        self.last_param_1 = param_1
        self.last_param_2 = param_2

    def stop_worker(self):
        pass


class DummyWorkerTaskQueueModule(Module):

    def configure(self, binder):
        worker = DummyWorker()
        binder.bind(TaskQueueWorker, to=worker, scope=singleton)


class DummyWorkerContainer(CoreContainer):
    dummy_worker = DummyWorkerTaskQueueModule


class RunDummyWorkerWithParamsTestCase(ZslTestCase, TestCase):
    CONFIG = IN_MEMORY_DB_SETTINGS.copy()
    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        app_name='RunDummyWorkerWithParamsTestCase', container=DummyWorkerContainer,
        config_object=CONFIG)

    _PARAM_1_TEST_VALUE = 1
    _PARAM_2_TEST_VALUE = 'Dont forget to read some good books!'

    @inject(worker=TaskQueueWorker)
    def testWorkerRunCountAndRunParams(self, worker):
        self.assertEqual(worker.run_count, 0, "worker.run() shouldn't be called yet.")

        run_worker(self._PARAM_1_TEST_VALUE, param_2=self._PARAM_2_TEST_VALUE)

        self.assertEqual(worker.run_count, 1, "worker.run() should be called exactly once.")
        self.assertEqual(worker.last_param_1, self._PARAM_1_TEST_VALUE, "worker.run() has obtained incorrect parameter 'param_1'.")
        self.assertEqual(worker.last_param_2, self._PARAM_2_TEST_VALUE, "worker.run() has obtained incorrect parameter 'param_2'.")
