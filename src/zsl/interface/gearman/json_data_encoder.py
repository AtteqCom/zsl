"""
:mod:`zsl.interface.gearman.json_data_encoder`
----------------------------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals

import json
import gearman
from zsl.db.model.app_model_json_encoder import AppModelJSONEncoder


class JSONDataEncoder(gearman.DataEncoder):
    @classmethod
    def encode(cls, encodable_object):
        return json.dumps(encodable_object, cls=AppModelJSONEncoder)

    @classmethod
    def decode(cls, decodable_string):
        return json.loads(decodable_string)
