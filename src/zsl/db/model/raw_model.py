"""
:mod:`zsl.db.model.raw_model`
-----------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals

from builtins import object

from zsl.utils.model_helper import update_model


class ModelBase(object):
    def update(self, app_model, forbidden_keys=None, inverse=False):
        """
        Updates the raw model. Consult `zsl.utils.model_helper.update_model`.
        """
        if forbidden_keys is None:
            forbidden_keys = []

        update_model(self, app_model, forbidden_keys, inverse)

    def get_app_model(self, id_name='id', hints=None):
        return self.__app_model__(self.__dict__, id_name, hints)
