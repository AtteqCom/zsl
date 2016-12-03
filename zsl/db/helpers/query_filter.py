from sqlalchemy.sql import func
#from zsl.application.service_application import service_application

class OperatorEq:
    def apply(self, q, attr, v):
        return q.filter(attr == v)

class OperatorNeq:
    def apply(self, q, attr, v):
        return q.filter(attr != v)

class OperatorLike:
    def apply(self, q, attr, v):
        return q.filter(attr.like(u'%{0}%'.format(v)))

class OperatorLeftLike:
    '''
        Left side of string is like ...
    '''
    def apply(self, q, attr, v):
        return q.filter(attr.like(u'{0}%'.format(v)))

class OperatorRightLike:
    '''
        Right side of string is like ...
    '''
    def apply(self, q, attr, v):
        return q.filter(attr.like(u'%{0}'.format(v)))

class OperatorBetween:
    def apply(self, q, attr, v):
        return q.filter(attr.between(v[0], v[1]))


class OperatorCompareDates:
    '''
        Compares only dates, year is not taken into account.
        Compared date value must be string in format '%m-%d'
    '''

    def apply(self, q, attr, v):
        return q.filter(func.date_format(attr, '%m-%d') == v)

class RelationshipOperatorContains:
    def apply(self, q, attr, v):
        return q.filter(attr.contains(v))


FILTER_HINT = 'hint'
FILTER_VALUES = 'values'

class QueryFilter(object):
    '''
    Helper class for applying filter criteria to query.
    '''

    def __init__(self, query_filter, mappings = [], allow_null = False):
        '''
        query_filter = {FILTER_VALUES: dict, FILTER_HINT: dict}
                - FILTER_VALUES dictionary (see example)
                - FILTER_HINTS dictionary - tells which operator (OperatorEq, OperatorBetween, ...)
                    use to which key from FILTER_VALUES dictionary
        mappings dict - maps keys from FILTER_VALUES to column attributes names of objects (see example)
                      - if the key from FILTER_VALUES is equal to the name of column attribute,
                        it doesn`t have to be mentioned in mappings
        allow_null boolean - if False (default value), None values from FILTER_VALUES will be ignored

        Example:
            query_filter = {
                FILTER_VALUES: {'fullname': 'jessica', 'lastname_initial': None},
                FILTER_HINT: {
                    'fullname': OperatorLike,
                    'lastname_initial': OperatorLeftLike,
                    'exclude_cid': OperatorNeq,
                }
            }
            mappings = {
                'lastname_initial': (Celebrity, 'lastname'),
                'exclude_cid': (Celebrity, 'cid'),
            }

            Notes: - 'fullname' key from FILTER_VALUES corresponds to column attribute Celebrity.fullname,
                    it doesn`t have to be mentioned in mappings
                  - if allow_null == False, key 'lastname_initial' from FILTER_VALUES will be ignored
                  - Celebrity is a sqlalechemy db model
        '''

        self._query_filter = query_filter
        self._allow_null = allow_null
        self._mappings = mappings

    def apply_query_filter(self, q, cls):
        hints = self._query_filter[FILTER_HINT]
        values = self._query_filter[FILTER_VALUES]

        for (k, v) in values.items():
            if v == None and not self._allow_null:
                continue

            if k in self._mappings:
                (cls, field) = self._mappings[k]
                attr = getattr(cls, field)
            else:
                attr = getattr(cls, k)

            q = hints[k]().apply(q, attr, v)

        return q
