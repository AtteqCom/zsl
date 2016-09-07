from sqlalchemy.ext.declarative.api import declarative_base
from asl.db.model.app_model import AppModel
from asl.db.model.raw_model import ModelBase
from sqlalchemy.sql.sqltypes import VARCHAR, INTEGER
from sqlalchemy.sql.schema import Column
from asl.utils.injection_helper import inject
from sqlalchemy.engine.base import Engine
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


@inject(engine=Engine, session_holder=SessionHolder)
def create_resource_test_data(engine, session_holder):
    Base.metadata.create_all(engine)
    session = session_holder()

    for dummy in dummies:
        session.add(DummyModel(id=dummy[0], val=dummy[1]))

    session.commit()
    session.close()
