'''
Created on Jan 6, 2014

one base the rule them all

.. moduleauthor:: Peter Morihladko
'''

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import Engine
from asl.application.service_application import service_application

DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata
metadata.bind = service_application.get_injector().get(Engine)