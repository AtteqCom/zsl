'''
Created on 28.3.2013

@author: Martin Babka
'''
#import abc

class AppModel:

#    @abc.abstractmethod
#    def get_id(self):
#        pass

    def __init__(self, raw):
        for (k, v) in raw.items():
            if not isinstance(v, (type(None), str, int, long, float, bool, unicode)):
                continue
            setattr(self, k, v)
