from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.engine
from application import service_application
import db.models.app
from sqlalchemy.orm import relationship, backref

if not service_application.is_initialized():
    print "Application is not initialized."
    quit()

DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata
metadata.bind = service_application.get_injector().get(sqlalchemy.engine.Engine)


class SportClub(DeclarativeBase):
    __tablename__ = 'sport_club'

    __table_args__ = {}

    #column definitions
    achievements = Column(u'achievements', TEXT())
    active = Column(u'active', INTEGER(length=1), nullable=False)
    added = Column(u'added', DATETIME(), nullable=False)
    city = Column(u'city', VARCHAR(length=255), nullable=False)
    coach = Column(u'coach', VARCHAR(length=255), nullable=False)
    created = Column(u'created', DATETIME())
    current_squad = Column(u'current_squad', INTEGER(length=1), nullable=False)
    flag_created_year = Column(u'flag_created_year', INTEGER(length=1), nullable=False)
    homepage = Column(u'homepage', VARCHAR(length=255), nullable=False)
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False)
    info = Column(u'info', TEXT())
    league = Column(u'league', VARCHAR(length=255), nullable=False)
    magazine_id = Column(u'magazine_id', INTEGER(), nullable=False)
    name = Column(u'name', VARCHAR(length=255), nullable=False)
    president = Column(u'president', VARCHAR(length=255), nullable=False)
    regexp = Column(u'regexp', TEXT(), nullable=False)
    sport_id = Column(u'sport_id', INTEGER(), ForeignKey('sport.id'), nullable=False)
    stadium = Column(u'stadium', VARCHAR(length=255), nullable=False)
    state_id = Column(u'state_id', INTEGER(), ForeignKey('state.id'), nullable=False)
    url = Column(u'url', VARCHAR(length=255), nullable=False)

    #relation definitions
    sport = relationship("Sport", backref=backref("sport_clubs", order_by=id))
    state = relationship("State", backref=backref("sport_clubs", order_by=id))

    def get_app_model(self):
        return db.models.app.SportClub(self.__dict__)


class State(DeclarativeBase):
    __tablename__ = 'state'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False)
    name_en = Column(u'name_en', VARCHAR(length=64), nullable=False)
    name_sk = Column(u'name_sk', VARCHAR(length=64), nullable=False)

    #relation definitions

    def get_app_model(self):
        return db.models.app.State(self.__dict__)


class Sport(DeclarativeBase):
    __tablename__ = 'sport'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False)
    name = Column(u'name', VARCHAR(length=255), nullable=False)

    #relation definitions

    def get_app_model(self):
        return db.models.app.Sport(self.__dict__)
