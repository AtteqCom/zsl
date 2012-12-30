from sqlalchemy import desc, asc

DEFAULT_SORT_ORDER = 'ASC' # If changed, look at the condition in apply_sorter if self.get_order() == "DESC":.

class Sorter(object):

    def __init__(self, sorter):
        if 'sortby' in sorter:
            self.__field = sorter['sortby']

            if 'sort' in sorter:
                self.__order = sorter['sort']
            else:
                self.__order = DEFAULT_SORT_ORDER

            self.__enabled = True
        else:
            self.__enabled = False

    def is_enabled(self):
        return self.__enabled

    def get_order(self):
        return self.__order

    def get_field(self):
        return self.__field

    def apply_sorter(self, q, cls):
        if self.is_enabled():
            attr = getattr(cls, self.get_field())
            if self.get_order() == "DESC": # If changed, look at the DEFAULT_SORT_ORDER definition.
                return q.order_by(desc(attr))
            else:
                return q.order_by(asc(attr))
        else:
            return q
