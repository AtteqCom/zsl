'''
Created on 28.3.2013

@author: Martin Babka
'''

class AppModel:
    '''
    ``AppModel``s are used as a thin and simple communication objects. Also they can be saved into cache.
    '''

    def __init__(self, raw, id_name = 'id'):
        self.set_from_raw_data(raw)

        self._id_name = id_name

    def set_from_raw_data(self, raw):
        for (k, v) in raw.items():
            if not isinstance(v, (type(None), str, int, long, float, bool, unicode)):
                continue
            setattr(self, k, v)

    def get_id(self):
        return self.__dict__[self._id_name]

    def _set_id_name(self, id_name):
        self._id_name = id_name

