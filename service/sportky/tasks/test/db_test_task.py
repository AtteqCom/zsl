'''
Created on 24.12.2012

@author: Martin Babka
'''

from injector import inject
import sqlalchemy
from application import service_application

class DbTestTask(object):

    @inject(db=sqlalchemy.engine.Engine)
    def __init__(self, db):
        self.__db = db
        service_application.logger.debug("Call from DbTestTesk.__init__, db {0}".format(db))

    def perform(self, data):
        return "{0}".format(self.__db.execute("select 1 * 2 * 3").scalar())
