"""
:mod:`zsl.db.helpers.pagination`
--------------------------------
"""
from __future__ import unicode_literals
from builtins import object

from sqlalchemy.orm.query import Query

FIRST_PAGE = 1
DEFAULT_PAGE_RECORD_COUNT = 25


class Pagination(object):
    def __init__(self, pagination=None):
        pagination = self._create_pagination_model(pagination)
        assert isinstance(pagination, PaginationModel)
        self._offset = (pagination.page_no - FIRST_PAGE) * pagination.page_record_count
        self._page_record_count = pagination.page_record_count
        self._record_count = 0

    def _create_pagination_model(self, pagination):
        if pagination is None:
            pagination = PaginationModel()
        elif isinstance(pagination, dict):
            page_record_count = int(pagination.get('page_record_count', DEFAULT_PAGE_RECORD_COUNT))
            pagination = PaginationModel(FIRST_PAGE + int(pagination.get('offset', 0)) // page_record_count,page_record_count)
        return pagination

    def set_record_count(self, record_count):
        self._record_count = record_count

    def get_record_count(self):
        return self._record_count

    def get_page_record_count(self):
        return self._page_record_count

    def get_offset(self):
        count = self.get_record_count()
        per_page = self.get_page_record_count()
        if self._offset >= count:
            last_page_size = count % per_page
            if last_page_size == 0:
                last_page_size = per_page
            self._offset = count - last_page_size
        if self._offset < 0:
            self._offset = 0

        return self._offset

    def apply_pagination(self, q):
        # type: (Query)->Query
        return q.limit(self.get_page_record_count()).offset(self.get_offset())

    def paginate(self, q):
        self.set_record_count(q.count())
        return self.apply_pagination(q).all()


class PaginationModel(object):
    def __init__(self, page_no=FIRST_PAGE,
                 page_record_count=DEFAULT_PAGE_RECORD_COUNT):
        self.page_no = int(page_no if page_no else FIRST_PAGE)
        self.page_record_count = int(
            page_record_count if page_record_count else DEFAULT_PAGE_RECORD_COUNT)
