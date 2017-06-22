"""
:mod:`zsl.db.model.app_model_json_encoder`
------------------------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals
from json.encoder import JSONEncoder
from zsl.db.model import AppModel


class AppModelJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, AppModel):
            d = dict(o.__dict__)
            for k in o._not_serialized_attributes:
                if k in d:
                    d.pop(k)
            return d
        else:
            return JSONEncoder.default(self, o)
