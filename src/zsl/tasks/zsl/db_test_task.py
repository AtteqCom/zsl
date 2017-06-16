"""
:mod:`zsl.tasks.asl.db_test_task`
---------------------------------

Created on 24.12.2012

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals

from builtins import object
from injector import inject
import sqlalchemy.engine
from zsl import Zsl
from flask import Response


class DbTestTask(object):
    """
    Connects to a database and executes a simple query. The result of the query should be 6.

    <emph>Input</emph>
    No input.

    <emph>Output</emph>
    Returns just a number 6.

    @author: Martin Babka
    """

    @inject(db=sqlalchemy.engine.Engine, app=Zsl)
    def __init__(self, db, app):
        self._db = db
        self._app = app
        self._app.logger.debug("Call from DbTestTesk.__init__, db {0}".format(db))

    def perform(self, data):
        return Response("{0}".format(self._db.execute("select 1 * 2 * 3").scalar()), mimetype='text/plain')
