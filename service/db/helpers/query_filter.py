class OperatorEq:
    def apply(self, q, attr, v):
        return q.filter(attr == v)

class OperatorLike:
    def apply(self, q, attr, v):
        return q.filter(attr.like('%{0}%'.format(v)))

FILTER_HINT = 'hint'
FILTER_VALUES = 'values'

class QueryFilter(object):

    def __init__(self, query_filter):
        self.__query_filter = query_filter

    def apply_query_filter(self, q, cls):
        hints = self.__query_filter[FILTER_HINT]
        values = self.__query_filter[FILTER_VALUES]

        for (k, v) in values.items():
            if v == None:
                continue

            attr = getattr(cls, k)
            q = hints[k]().apply(q, attr, v)

        return q
