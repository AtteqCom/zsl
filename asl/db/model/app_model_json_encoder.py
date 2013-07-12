'''
Created on 28.3.2013

@author: Martin Babka
'''
from json.encoder import JSONEncoder
from asl.db.model import AppModel

class AppModelJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, AppModel):
            d = dict(o.__dict__)
            for k in o._not_serialized_attributes:
                d.pop(k)
            return d
        else:
            return JSONEncoder.default(self, o)


