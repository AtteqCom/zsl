'''
Created on May 14, 2014

.. moduleauthor:: peter
'''
import unittest

from sqlalchemy import create_engine, VARCHAR, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.engine.base import Engine

from injector import Module, singleton, Injector

from asl.resource.model_resource import ModelResource
from asl.db.model.raw_model import ModelBase
from asl.db.model.app_model import AppModel
from asl.application.initializers.database_initializer import SessionHolder

Base = declarative_base()

class DummyAppModel(AppModel):
    pass

class DummyModel(Base, ModelBase):
    __tablename__ = 'dummy'
    
    _app_model_class = DummyAppModel
    
    id = Column('id', INTEGER(), primary_key=True, nullable=False)
    val = Column('val', VARCHAR(length=15), nullable=False)
     
dummies = [
  (1, 'one'),
  (2, 'two'),
  (3, 'three'),
  (4, 'four'),
  (5, 'five'),
  (6, 'six'),
  (7, 'seven'),
  (8, 'eight'),
  (9, 'nine'),
  (10, 'ten')
]

def configure_test(binder):
    engine = create_engine('sqlite://')

    session = SessionHolder(sessionmaker(engine, autocommit=False, expire_on_commit=False))
    binder.bind(
        SessionHolder,
        to = session,
        scope = singleton
    )
    
    binder.bind(
        Engine,
        to = engine,
        scope = singleton
    )
    
    

class TestModelResource(unittest.TestCase):

    def setUp(self):
        
        # toto nekopirovat, zatial je to iba ako koncept, ktory 
        # treba rozsirit do niecoho znovu pouzitelneh
        self._injector = Injector([configure_test])
        Base.metadata.create_all(self._injector.get(Engine))

        session = self._injector.get(SessionHolder)()
        
        for dummy in dummies:
            session.add(DummyModel(id=dummy[0], val=dummy[1]))
            
        session.commit()
        session.close()
        
        self.resource = self._injector.create_object(ModelResource, {'model_cls': DummyModel})

    def tearDown(self):
        pass

    def testRead(self):
        m = self.resource.read('9')
        self.assertEqual('nine', m.val, "Read one")
        
        m = self.resource.read(args={'limit': 'unlimited'})


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()