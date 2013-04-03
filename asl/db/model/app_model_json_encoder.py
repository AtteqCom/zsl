'''
Created on 28.3.2013

@author: Martin Babka
'''
from json.encoder import JSONEncoder
from asl.db.model import AppModel

class AppModelJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, AppModel):
            return o.__dict__
        else:
            return JSONEncoder.default(self, o)
