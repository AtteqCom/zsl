from __future__ import absolute_import
from __future__ import unicode_literals

from sqlalchemy.engine import Engine

from zsl import inject
from zsl.db.model.sql_alchemy import metadata


class DbTestCase:
    @inject(engine=Engine)
    def createSchema(self, engine):
        metadata.bind = engine
        metadata.create_all(engine)
