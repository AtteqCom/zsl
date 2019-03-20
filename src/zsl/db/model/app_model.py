"""
:mod:`zsl.db.model.app_model`
-----------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals

# noinspection PyCompatibility
from builtins import map, object

from future.utils import viewitems

from zsl.utils.dict_to_object_conversion import extend_object_by_dict

DATE_DATA = 'date_data'
DATETIME_DATA = 'datetime_data'
RELATED_FIELDS = 'related_fields'
RELATED_FIELDS_CLASS = 'cls'
RELATED_FIELDS_HINTS = 'hints'

ISO_8601_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


class AppModel(object):
    """AppModel's are used as a thin and simple communication objects. Also
    they can be saved into cache. Basically they are known as Data Transfer
    Objects or DTOs.

    .. automethod:: __init__
    """

    _not_serialized_attributes = ['_not_serialized_attributes', '_hints',
                                  '_id_name']

    def __init__(self, raw, id_name='id', hints=None):
        """
        The application model model constructor.

        :param raw: Dictionary of properties of the raw data.
        :param id_name: Name of the identifier property.
        :param hints: Tells which of the raw attributes are date or datetime
                      string and what is theirs format. Example:
                      ```
                      {
                          DATE_DATA: { 'birthday': '%d.%m.%Y' },
                          DATETIME_DATA: { 'created': '%Y-%m-%d %H:%M:%S' }
                      }
                      ```
                      this attributes are then saved in the standard zsl
                      service date/datetime format (consult
                      :mod:`zsl.utils.date_helper` for more.)
        """

        extend_object_by_dict(self, raw, hints)
        self._id_name = id_name

    def get_id(self):
        return self.__dict__[self._id_name]

    def _set_id_name(self, id_name):
        self._id_name = id_name

    @staticmethod
    def convert(v):
        if isinstance(v, AppModel):
            return v.get_attributes()
        else:
            return v

    def get_attributes(self):
        d = dict(self.__dict__)

        for k in self.__dict__:
            if k in self._not_serialized_attributes:
                d.pop(k)

            elif isinstance(d[k], AppModel):
                d[k] = self.convert(d[k])

            elif isinstance(d[k], list):
                d[k] = list(map(self.convert, d[k]))

            elif isinstance(d[k], tuple):
                d[k] = list(map(self.convert, d[k]))
                d[k] = tuple(d[k])

            elif isinstance(d[k], dict):
                for key, value in viewitems(getattr(self, k)):
                    d[k][key] = self.convert(value)

        return d

    def __str__(self):
        return "{0}: {1}".format(self.__class__, self.__dict__)
