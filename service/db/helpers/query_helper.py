'''
Created on 30.12.2012

@author: Martin Babka
'''
from db.helpers.pagination import Pagination
from db.helpers.sorter import Sorter
from db.helpers.query_filter import QueryFilter

class QueryHelper(object):

    def __init__(self, cls, query_filter, pagination, sorter):
        self.__cls = cls

        if not isinstance(query_filter, QueryFilter):
            query_filter = QueryFilter(query_filter)
        self.__query_filter = query_filter

        if not isinstance(pagination, Pagination):
            pagination = Pagination(pagination)
        self.__pagination = pagination

        if not isinstance(sorter, Sorter):
            sorter = Sorter(sorter)
        self.__sorter = sorter

    def execute(self, q):
        q = self.__query_filter.apply_query_filter(q, self.__cls)
        q = self.__sorter.apply_sorter(q, self.__cls)
        return self.__pagination.paginate(q)

    def get_pagination(self):
        return self.__pagination

    def get_sorter(self):
        return self.__sorter
