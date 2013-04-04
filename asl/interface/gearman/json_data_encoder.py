'''
Created on 22.12.2012

@author: Martin Babka
'''
import json
import gearman
from asl.db.model.app_model_json_encoder import AppModelJSONEncoder

class JSONDataEncoder(gearman.DataEncoder):
    @classmethod
    def encode(cls, encodable_object):
        return json.dumps(encodable_object, cls = AppModelJSONEncoder)

    @classmethod
    def decode(cls, decodable_string):
        return json.loads(decodable_string)
