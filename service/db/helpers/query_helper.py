'''
Created on 30.12.2012

@author: Martin Babka
'''
from db.helpers.pagination import Pagination
from db.helpers.sorter import Sorter
from db.helpers.query_filter import QueryFilter

class QueryHelper(object):

    def __init__(self, cls, query_filter, pagination, sorter):
        self._cls = cls

        if not isinstance(query_filter, QueryFilter):
            query_filter = QueryFilter(query_filter)
        self._query_filter = query_filter

        if not isinstance(pagination, Pagination):
            pagination = Pagination(pagination)
        self._pagination = pagination

        if not isinstance(sorter, Sorter):
            sorter = Sorter(sorter)
        self._sorter = sorter

    def execute(self, q):
        q = self._query_filter.apply_query_filter(q, self._cls)
        q = self._sorter.apply_sorter(q, self._cls)
        return self._pagination.paginate(q)

    def get_pagination(self):
        return self._pagination

    def get_sorter(self):
        return self._sorter
