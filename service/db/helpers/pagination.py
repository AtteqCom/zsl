DEFAULT_PAGE_RECORD_COUNT = 25

class Pagination(object):

    def __init__(self, pagination):
        if 'offset' in pagination:
            self.__offset = int(pagination['offset'])
        else:
            self.__offset = 0

        if 'page_record_count' in pagination:
            self.__page_record_count = int(pagination['page_record_count'])
        else:
            self.__page_record_count = DEFAULT_PAGE_RECORD_COUNT

        self.__record_count = 0

    def set_record_count(self, record_count):
        self.__record_count = record_count

    def get_record_count(self):
        return self.__record_count

    def get_page_record_count(self):
        return self.__page_record_count

    def get_offset(self):
        if self.__offset >= self.get_record_count():
            self.__offset = max(self.get_record_count() - 1, 0)

        return self.__offset

    def apply_pagination(self, q):
        return q.limit(self.get_page_record_count()).offset(self.get_offset())

    def paginate(self, q):
        self.set_record_count(q.count())
        return self.apply_pagination(q).all()
