"""
:mod:`zsl.tasks.asl.test_task`
------------------------------

Created on 22.12.2012

..moduleauthor:: Martin Babka <babka@atteq.com>
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from builtins import *


class TestTask(object):
    def perform(self, _data):
        logging.getLogger(__name__).debug("Running zsl.tasks.zsl.TestTask")
        return "ok"
