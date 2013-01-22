'''
Created on 24.12.2012

@author: Martin Babka
'''

from injector import inject
import sqlalchemy.engine
from application import service_application

class DbTestTask(object):
    '''
    Connects to a database and executes a simple query. The result of the query should be 6.

    <emph>Input</emph>
    No input.

    <emph>Output</emph>
    Returns just a number 6.

    @author: Martin Babka
    '''

    @inject(db=sqlalchemy.engine.Engine)
    def __init__(self, db):
        self.__db = db
        service_application.logger.debug("Call from DbTestTesk.__init__, db {0}".format(db))

    def perform(self, data):
        return "{0}".format(self.__db.execute("select 1 * 2 * 3").scalar())
