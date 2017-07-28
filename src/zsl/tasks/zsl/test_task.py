"""
:mod:`zsl.tasks.asl.test_task`
------------------------------

Created on 22.12.2012

..moduleauthor:: Martin Babka <babka@atteq.com>
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from builtins import *

import logging

from zsl import Zsl
from injector import inject


class TestTask(object):

    @inject(app=Zsl)
    def __init__(self, app):
        self._app = app

    def perform(self, _data):
        logging.getLogger(__name__).debug("Running zsl.tasks.zsl.TestTask")
        return "ok"
