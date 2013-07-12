'''
Created on 28.3.2013

@author: Martin Babka
'''

from datetime import datetime, date
from asl.utils.date_helper import format_date_portable, format_datetime_portable

DATE_DATA = 'date_data'
DATETIME_DATA = 'datetime_data'

class AppModel:
    '''
    ``AppModel``s are used as a thin and simple communication objects. Also they can be saved into cache.
    '''

    _not_serialized_properties = ['_not_serialized_properties', '_hints', '_id_name']

    def __init__(self, raw, id_name = 'id', hints = None):
        '''
        The application model model constructor.

        @param raw: Dictionary of properties of the raw data.
        @param id_name: Name of the identifier property.
        @param hints: Tells which of the raw attributes are date or datetime string and what is theirs format
                      Example: {DATE_DATA: {'birthday': '%d.%m.%Y'}, DATETIME_DATA: {'created': '%Y-%m-%d %H:%M:%S'}}
                      this attributes are then saved in the standard asl service date/datetime format (consult asl.utils.date_helper)
        '''

        if hints == None:
            self._hints = {DATE_DATA: {}, DATETIME_DATA: {}}
        else:
            self._hints = hints
            if not DATE_DATA in self._hints:
                self._hints[DATE_DATA] = {}
            if not DATETIME_DATA in self._hints:
                self._hints[DATETIME_DATA] = {}

        self.set_from_raw_data(raw)
        self._id_name = id_name

    def set_from_raw_data(self, raw):
        for (k, v) in raw.items():
            if isinstance(v, (type(None), str, int, long, float, bool, unicode)):
                if k in self._hints[DATE_DATA]:
                    d = datetime.strptime(v, self._hints[DATE_DATA][k]).date()
                    setattr(self, k, format_date_portable(d))
                elif k in self._hints[DATETIME_DATA]:
                    d = datetime.strptime(v, self._hints[DATETIME_DATA][k])
                    setattr(self, k, format_datetime_portable(d))
                else:
                    setattr(self, k, v)
            elif isinstance(v, datetime):
                setattr(self, k, format_datetime_portable(v))
            elif isinstance(v, date):
                setattr(self, k, format_date_portable(v))

    def get_id(self):
        return self.__dict__[self._id_name]

    def _set_id_name(self, id_name):
        self._id_name = id_name

