"""
:mod:`zsl.db.helpers.sorter`
----------------------------
"""
from __future__ import unicode_literals
from builtins import zip
from builtins import object
from sqlalchemy import desc, asc

DEFAULT_SORT_ORDER = 'ASC'  # If changed, look at the condition in apply_sorter if self.get_order() == "DESC":.


class Sorter(object):
    """
    Helper class for applying ordering criteria to query.
    """

    def __init__(self, sorter, mappings=None):
        """
        sorter = {'sortby': string, 'sort': string}
            sortby - string of comma-separated column names by which you want to order
            sort - string of comma-separated values 'ASC'/'DESC' (order direction) which
                    set order direction to corresponding columns from sorter['sortby'] string
            notes: - if 'sortby' key is not in sorter, no sorting will be applied to query
                   - if 'sort' key is not in sorter, DEFAULT_SORT_ORDER will be applied to
                     all columns from sorter['sortby']
                   - if sorter['sort'] == 'ASC' / 'DESC' (contains only one order direction),
                     this direction will be applied to all columns from sorter['sortby']
                   - if you want to order only by one column, simply put
                     sorter['sortby'] = '<column_name>' - without comma at the end of
                     the string
        mappings dict - maps column names from sorter['sortby'] to column attributes names of
                        objects (see example)
                      - if the column names from sorter['sortby'] is equal to the name
                        of column attribute, it doesn`t have to be mentioned in mappings

        Example:
            sorter = {'sortby': 'firstname,state,sport', 'sort': 'ASC'}

            mappings = {
                'state': (State, 'name_sk'),
                'sport': (Sport, 'name'),
            }

        """
        if mappings is None:
            mappings = []

        if 'sortby' in sorter:
            self._fields = sorter['sortby'].split(',')

            if 'sort' in sorter:
                self._orders = sorter['sort'].split(',')
                if len(self._orders) == 1:
                    self._orders *= len(self._fields)
                elif len(self._orders) != len(self._fields):
                    raise Exception(
                        'zsl.db.helpers.Sorter: Number of order settings is nor zero nor one nor equal to number of'
                        'sortby columns.')

            else:
                self._orders = [DEFAULT_SORT_ORDER] * len(self._fields)

            self._enabled = True
        else:
            self._enabled = False

        self._mappings = mappings

    def is_enabled(self):
        return self._enabled

    def get_fields(self):
        return self._fields

    def get_orders(self):
        return self._orders

    def apply_sorter(self, q, cls):
        if self.is_enabled():
            sorter_settings = []
            for field, order in zip(self.get_fields(), self.get_orders()):
                if field in self._mappings:
                    (cls, mapped_field) = self._mappings[field]
                    attr = getattr(cls, mapped_field)
                else:
                    attr = getattr(cls, field)
                if order == "DESC":  # If changed, look at the DEFAULT_SORT_ORDER definition.
                    sorter_settings.append(desc(attr))
                else:
                    sorter_settings.append(asc(attr))

            return q.order_by(*sorter_settings)
        else:
            return q
