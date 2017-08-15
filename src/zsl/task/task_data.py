"""
:mod:`zsl.task.task_data`
-------------------------

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import *

from zsl import Injected
from zsl import Zsl
from zsl import inject
from zsl.utils.warnings import deprecated


class TaskData(object):
    @inject(app=Zsl)
    def __init__(self, payload, app=Injected, payload_type=str):
        self._app = app
        self._payload = payload
        self._payload_type = payload_type

    @deprecated
    def get_data(self):
        return self._payload

    @property
    def payload(self):
        return self._payload

    def transform_payload(self, f):
        self._payload = f(self._payload) if self._payload is not None else {}
