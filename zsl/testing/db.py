from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from sqlalchemy.engine import Engine

from zsl import inject
from zsl.db.model.sql_alchemy import metadata


class DbTestCase(object):
    @inject(engine=Engine)
    def createSchema(self, engine):
        metadata.bind = engine
        metadata.create_all(engine)


