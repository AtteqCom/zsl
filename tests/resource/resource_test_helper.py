"""
Fixtures and helper functions to test models and test resources
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *  # NOQA
from collections import namedtuple

from sqlalchemy import ForeignKey
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from zsl.application.modules.alchemy_module import SessionHolder
from zsl.db.model.app_model import AppModel
from zsl.db.model.raw_model import ModelBase
from zsl.utils.injection_helper import inject

Base = declarative_base()


class UserAppModel(AppModel):
    pass


class UserModel(Base, ModelBase):
    __tablename__ = 'users'
    __app_model__ = UserAppModel

    id = Column('id', Integer, primary_key=True, nullable=False)
    name = Column('name', String, nullable=False)

    def __repr__(self):
        return '<User(id=\'{}\',name=\'{}\')>'.format(self.id, self.name)

UserTuple = namedtuple('UserTuple', 'id name')

users = [
    UserTuple(1, 'one'),
    UserTuple(2, 'two'),
    UserTuple(3, 'three'),
    UserTuple(4, 'four'),
    UserTuple(5, 'five'),
    UserTuple(6, 'six'),
    UserTuple(7, 'seven'),
    UserTuple(8, 'eight'),
    UserTuple(9, 'nine'),
    UserTuple(10, 'ten'),
    UserTuple(11, 'one'),
    UserTuple(12, 'two'),
    UserTuple(13, 'three'),
    UserTuple(14, 'four'),
    UserTuple(15, 'five'),
    UserTuple(16, 'six'),
    UserTuple(17, 'seven'),
    UserTuple(18, 'eight'),
    UserTuple(19, 'nine'),
    UserTuple(20, 'ten')
]


class AddressAppModel(AppModel):
    pass


class AddressModel(Base, ModelBase):
    __tablename__ = 'addresses'
    __app_model__ = AddressAppModel

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('UserModel', back_populates='addresses')

    def __repr__(self):
        return '<Address(email_address=\'{}\')>'.format(self.email_address)

UserModel.addresses = relationship('AddressModel', order_by=AddressModel.id, back_populates='user')


AddressTuple = namedtuple('AddressTuple', 'id email_address user_id')

addresses = [
    AddressTuple(1, 'knutley0@reverbnation.com', 1),
    AddressTuple(2, 'zlerwell1@aboutads.info', 1),
    AddressTuple(3, 'ereap2@deviantart.com', 2),
]


def get_non_existent_id():
    """Return an id for non existent user."""
    return len(users) + 10


@inject(engine=Engine, session_holder=SessionHolder)
def create_resource_test_data(engine, session_holder):
    Base.metadata.create_all(engine)
    session = session_holder()

    for u in users:
        session.add(UserModel(**u._asdict()))

    for a in addresses:
        session.add(AddressModel(**a._asdict()))

    session.commit()
    session.close()
