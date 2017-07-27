"""
:mod:`zsl.tasks.asl.test_task`
------------------------------

Created on 22.12.2012

..moduleauthor:: Martin Babka <babka@atteq.com>
"""
from __future__ import unicode_literals

from builtins import object
from zsl.task.task_decorator import json_input, json_output
from zsl import Zsl
from injector import inject


class TestTask(object):

    @inject(app=Zsl)
    def __init__(self, app):
        self._app = app

    def perform(self, _data):
        return "ok"
