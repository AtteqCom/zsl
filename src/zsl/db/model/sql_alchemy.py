"""
:mod:`zsl.db.model.sql_alchemy`
-------------------------------

one base to rule them all

.. moduleauthor:: Peter Morihladko
"""
from sqlalchemy.ext.declarative import declarative_base

from zsl.db.model.raw_model import ModelBase

DeclarativeBase = declarative_base(cls=ModelBase)
metadata = DeclarativeBase.metadata
