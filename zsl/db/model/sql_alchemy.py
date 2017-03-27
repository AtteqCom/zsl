"""
:mod:`zsl.db.model.sql_alchemy`
-------------------------------

one base the rule them all

.. moduleauthor:: Peter Morihladko
"""
from __future__ import unicode_literals

from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata
