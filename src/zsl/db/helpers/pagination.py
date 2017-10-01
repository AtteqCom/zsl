"""
:mod:`zsl.db.helpers.pagination`
--------------------------------
"""
from __future__ import unicode_literals

from builtins import object
from typing import Dict, Union

from sqlalchemy.orm.query import Query

from zsl.db.model.app_model import AppModel

FIRST_PAGE = 1
DEFAULT_PAGE_SIZE = 25


class Pagination(object):
    """
    Pagination support. Allows to paginate a query. There are two choices.
      #. :meth:`.paginate` - paginates a query and obtains the count
         automatically.
      #. :meth:`.apply_pagination` - paginates a query and assumes that
         record count is set in advance.
    """

    def __init__(self, pagination=None):
        # type: (Union[PaginationRequest, Dict[str, Union[str, int]], None])->None
        pagination = self._create_pagination_request(pagination)
        assert isinstance(pagination, PaginationRequest)
        self._offset = (pagination.page_no - FIRST_PAGE) * pagination.page_size
        self._page_size = pagination.page_size
        self._record_count = -1

    def _create_pagination_request(self, pagination):
        # type: (Union[PaginationRequest, Dict[str, Union[str, int]], None])->PaginationRequest
        if pagination is None:
            pagination = PaginationRequest()
        elif isinstance(pagination, dict):
            page_size = int(pagination.get('page_size', DEFAULT_PAGE_SIZE))
            pagination = PaginationRequest(
                FIRST_PAGE + int(pagination.get('offset', 0)) // page_size,
                page_size)
        return pagination

    @property
    def record_count(self):
        return self._record_count

    @record_count.setter
    def record_count(self, record_count):
        self._record_count = record_count

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        # type: (int)->None
        self._page_size = page_size

    @property
    def offset(self):
        count = self._record_count
        per_page = self.page_size
        if self._offset >= count:
            last_page_size = count % per_page
            if last_page_size == 0:
                last_page_size = per_page
            self._offset = count - last_page_size
        if self._offset < 0:
            self._offset = 0

        return self._offset

    @offset.setter
    def offset(self, offset):
        # type:(int)->None
        self._offset = offset

    def apply_pagination(self, q):
        """
        Filters the query so that a given page is returned. The record count
        must be set in advance.
        :param q: Query to be paged.
        :return: Paged query.
        """
        # type: (Query)->Query
        assert self.record_count >= 0, "Record count must be set."
        return q.limit(self.page_size).offset(self.offset)

    def paginate(self, q):
        """
        Filters the query so that a given page is returned. The record count
        is computed automatically from query.
        :param q: Query to be paged.
        :return: Paged query.
        """
        self.record_count = q.count()
        return self.apply_pagination(q).all()


class PaginationRequest(AppModel):
    def __init__(self, page_no=FIRST_PAGE,
                 page_size=DEFAULT_PAGE_SIZE):
        super(PaginationRequest, self).__init__({})
        self.page_no = int(page_no) if page_no else FIRST_PAGE
        self.page_size = int(page_size) if page_size else DEFAULT_PAGE_SIZE


class PaginationResponse(AppModel):
    def __init__(self, record_count, page_size, pagination):
        # type: (int, int, PaginationRequest)->None
        super(PaginationResponse, self).__init__({})
        self.record_count = record_count
        max_page_size = pagination.page_size
        self.page_count = (record_count + max_page_size - 1) // max_page_size
        self.page_size = page_size
        self.max_page_size = max_page_size
        self.page_no = pagination.page_no
