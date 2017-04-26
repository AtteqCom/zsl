from collections import namedtuple

from sqlalchemy.ext.declarative.api import declarative_base
from zsl.db.model.app_model import AppModel
from zsl.db.model.raw_model import ModelBase
from sqlalchemy.sql.sqltypes import VARCHAR, INTEGER
from sqlalchemy.sql.schema import Column
from zsl.utils.injection_helper import inject
from sqlalchemy.engine.base import Engine
from zsl.application.modules.alchemy_module import SessionHolder

test_settings = {
    'DATABASE_URI': 'sqlite:///:memory:',
    'DATABASE_ENGINE_PROPS': {'echo': True},
}

Base = declarative_base()


class DummyAppModel(AppModel):
    pass


class DummyModel(Base, ModelBase):
    __tablename__ = 'dummy'

    _app_model_class = DummyAppModel

    id = Column('id', INTEGER(), primary_key=True, nullable=False)
    val = Column('val', VARCHAR(length=15), nullable=False)

DummyTuple = namedtuple('DummyTuple', ['id', 'val'])

dummies = [
    DummyTuple(1, 'one'),
    DummyTuple(2, 'two'),
    DummyTuple(3, 'three'),
    DummyTuple(4, 'four'),
    DummyTuple(5, 'five'),
    DummyTuple(6, 'six'),
    DummyTuple(7, 'seven'),
    DummyTuple(8, 'eight'),
    DummyTuple(9, 'nine'),
    DummyTuple(10, 'ten')
]


@inject(engine=Engine, session_holder=SessionHolder)
def create_resource_test_data(engine, session_holder):
    Base.metadata.create_all(engine)
    session = session_holder()

    for dummy in dummies:
        session.add(DummyModel(id=dummy[0], val=dummy[1]))

    session.commit()
    session.close()
