"""
:mod:`zsl.task.task_data`
-------------------------

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""
from typing import Type

from injector import noninjectable

from zsl import Zsl, inject
from zsl.utils.warnings import deprecated


class TaskData(object):

    @inject
    @noninjectable('payload_type')
    def __init__(self, payload: str, app: Zsl, payload_type: Type = str) -> None:
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
