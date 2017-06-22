"""
:mod:`zsl.db.model.sql_alchemy`
-------------------------------

one base the rule them all

.. moduleauthor:: Peter Morihladko
"""
from __future__ import unicode_literals

from sqlalchemy.ext.declarative import declarative_base

from zsl.db.model.raw_model import ModelBase

DeclarativeBase = declarative_base(cls=ModelBase)
metadata = DeclarativeBase.metadata
