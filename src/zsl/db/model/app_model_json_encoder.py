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
            return o.get_attributes()
        elif isinstance(o, object):
            return dict(o.__dict__)
        else:
            return JSONEncoder.default(self, o)
