'''
Created on 31.1.2013

@author: Martin Babka
'''
from sportky.service.service import Service, transactional
from db.models.raw import Image
from db.helpers.query_helper import QueryHelper
from db.helpers.sorter import Sorter

class ImageService(Service):
    '''
    Image service.
    '''

    def __init__(self):
        Service.__init__(self)

    @transactional
    def fetch_list(self, filter, pagination):
        qh = QueryHelper(Image, filter, pagination, Sorter({'sortby': 'created', 'sort': 'desc'}, {}))
        return (qh.execute(self._orm.query(Image)), qh)
