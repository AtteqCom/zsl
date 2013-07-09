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
            if "_id_name" in d:
                d.pop("_id_name")
            return d
        else:
            return JSONEncoder.default(self, o)


