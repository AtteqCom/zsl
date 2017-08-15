"""
:mod:`zsl.db.model.app_model`
-----------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals

# noinspection PyCompatibility
from builtins import int, map, object, str
from datetime import date, datetime

from future.utils import viewitems

from zsl.utils.date_helper import format_date_portable, format_datetime_portable

DATE_DATA = 'date_data'
DATETIME_DATA = 'datetime_data'
RELATED_FIELDS = 'related_fields'
RELATED_FIELDS_CLASS = 'cls'
RELATED_FIELDS_HINTS = 'hints'

ISO_8601_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


class AppModel(object):
    """AppModel's are used as a thin and simple communication objects. Also
    they can be saved into cache.

    .. automethod:: __init__
    """

    _not_serialized_attributes = ['_not_serialized_attributes', '_hints', '_id_name']

    def __init__(self, raw, id_name='id', hints=None):
        """
        The application model model constructor.

        :param raw: Dictionary of properties of the raw data.
        :param id_name: Name of the identifier property.
        :param hints: Tells which of the raw attributes are date or datetime string and what is theirs format \
        Example: ``{DATE_DATA: {'birthday': '%d.%m.%Y'}, DATETIME_DATA: {'created': '%Y-%m-%d %H:%M:%S' }}`` \
        this attributes are then saved in the standard zsl service date/datetime format (consult \
        zsl.utils.date_helper)
        """

        if hints is None:
            self._hints = {DATE_DATA: {}, DATETIME_DATA: {}, RELATED_FIELDS: {}}
        else:
            self._hints = hints
            if DATE_DATA not in self._hints:
                self._hints[DATE_DATA] = {}
            if DATETIME_DATA not in self._hints:
                self._hints[DATETIME_DATA] = {}
            if RELATED_FIELDS not in self._hints:
                self._hints[RELATED_FIELDS] = {}

        self.set_from_raw_data(raw)
        self._id_name = id_name

    def set_from_raw_data(self, raw):
        for k, v in viewitems(raw):
            if isinstance(v, (type(None), str, int, float, bool)):
                if k in self._hints[DATE_DATA] and v is not None:
                    d = datetime.strptime(v, self._hints[DATE_DATA][k]).date()
                    setattr(self, k, format_date_portable(d))
                elif k in self._hints[DATETIME_DATA] and v is not None:
                    d = datetime.strptime(v, self._hints[DATETIME_DATA][k])
                    setattr(self, k, format_datetime_portable(d))
                else:
                    setattr(self, k, v)
            elif isinstance(v, datetime):
                setattr(self, k, format_datetime_portable(v))
            elif isinstance(v, date):
                setattr(self, k, format_date_portable(v))
            elif k in self._hints[RELATED_FIELDS]:
                related_cls = self._hints[RELATED_FIELDS][k][RELATED_FIELDS_CLASS]
                related_hints = self._hints[RELATED_FIELDS][k].get(RELATED_FIELDS_HINTS)
                if isinstance(v, (list, tuple)):
                    setattr(self, k, [related_cls(x, 'id', related_hints) for x in v])
                else:
                    setattr(self, k, related_cls(v.__dict__, 'id', related_hints))

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
