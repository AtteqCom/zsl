"""
:mod:`zsl.tasks.asl.test_task`
------------------------------

Created on 22.12.2012

..moduleauthor:: Martin Babka <babka@atteq.com>
"""
import logging


class TestTask:
    def perform(self, _data):
        logging.getLogger(__name__).debug("Running zsl.tasks.zsl.TestTask")
        return "ok"
