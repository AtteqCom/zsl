"""
:mod:`zsl.testing.test_utils`
-----------------------------
Test utilities.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import json
from typing import Any

from zsl.task.task_data import TaskData


def parent_module(module_name):
    # type: (str) -> str
    """Return the parent module name for a module.

    :param module_name: module nam
    :type module_name: str
    :return: module's parent name
    :rtype: str

    >>> parent_module('zsl.application.module')
    'zsl.application'
    """
    return '.'.join(module_name.split('.')[:-1])


class TestTaskData(TaskData):
    """Data suitable when directly calling a task."""

    def __init__(self, data):
        # type: (Any)->None
        super(TestTaskData, self).__init__(json.dumps(data))
