class OperatorEq:
    def apply(self, q, attr, v):
        return q.filter(attr == v)

class OperatorNeq:
    def apply(self, q, attr, v):
        return q.filter(attr != v)

class OperatorLike:
    def apply(self, q, attr, v):
        return q.filter(attr.like('%{0}%'.format(v)))

class OperatorLeftLike:
    '''
        Left side of string is like ...
    '''
    def apply(self, q, attr, v):
        return q.filter(attr.like('{0}%'.format(v)))

class OperatorRightLike:
    '''
        Right side of string is like ...
    '''
    def apply(self, q, attr, v):
        return q.filter(attr.like('%{0}'.format(v)))

class OperatorBetween:
    def apply(self, q, attr, v):
        return q.filter(attr.between(v[0], v[1]))

class RelationshipOperatorContains:
    def apply(self, q, attr, v):
        return q.filter(attr.contains(v))

FILTER_HINT = 'hint'
FILTER_VALUES = 'values'

class QueryFilter(object):
    def __init__(self, query_filter, mappings = []):
        self._query_filter = query_filter
        self._mappings = mappings

    def apply_query_filter(self, q, cls):
        hints = self._query_filter[FILTER_HINT]
        values = self._query_filter[FILTER_VALUES]

        for (k, v) in values.items():
            if v == None:
                continue

            if k in self._mappings:
                (cls, field) = self._mappings[k]
                attr = getattr(cls, field)
            else:
                attr = getattr(cls, k)

            q = hints[k]().apply(q, attr, v)

        return q
