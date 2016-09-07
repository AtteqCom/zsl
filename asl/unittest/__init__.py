from asl.interface.importer import initialize_cli_application, InitializationContext
import unittest
import json
initialize_cli_application(InitializationContext(unit_test=True))

from asl.task.task_data import TaskData
from asl.utils.injection_helper import inject
from asl.application.service_application import AtteqServiceFlask


class TestCase(unittest.TestCase):

    pass


class TestTaskData(TaskData):

    @inject(service_application=AtteqServiceFlask)
    def __init__(self, data, service_application):
        TaskData.__init__(self, service_application, json.dumps(data))
