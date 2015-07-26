'''
:mod:`asl.db.model.raw_model`

.. moduleauthor:: Martin Babka
'''
from asl.utils.model_helper import update_model

class ModelBase:
    def update(self, app_model, forbidden_keys = [], inverse = False):
        '''
        Updates the raw model. Consult `asl.utils.model_helper.update_model`.
        '''
        update_model(self, app_model, forbidden_keys, inverse)

    def _set_app_model_class(self, app_model_class):
        self._app_model_class = app_model_class

    def get_app_model(self):
        return self._app_model_class(self.__dict__)
