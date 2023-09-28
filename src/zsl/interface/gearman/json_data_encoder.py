"""
:mod:`zsl.interface.gearman.json_data_encoder`
----------------------------------------------

.. moduleauthor:: Martin Babka
"""
import json

from zsl.db.model.app_model_json_encoder import AppModelJSONEncoder
from zsl.gearman import gearman


class JSONDataEncoder(gearman.DataEncoder):
    @classmethod
    def encode(cls, encodable_object):
        return json.dumps(encodable_object, cls=AppModelJSONEncoder)

    @classmethod
    def decode(cls, decodable_string):
        return json.loads(decodable_string)
