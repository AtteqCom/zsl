'''
Created on 28.3.2013

@author: Martin Babka
'''

class AppModel:
    def __init__(self, raw):
        for (k, v) in raw.items():
            if not isinstance(v, (type(None), str, int, long, float, bool, unicode)):
                continue
            setattr(self, k, v)