from task.task_decorator import json_output
from injector import inject
import sqlalchemy.orm
import logging

import xml.etree.ElementTree as xml
import random
import urllib2
import os.path

from db.models.raw import SportClub, SportClubField, Sport, State, Image
from sqlalchemy.sql.expression import asc

from utils import url_helper
from sportky.tasks.clubs.fetch_club_task import FetchClubTask
from application.service_application import service_application

XML_URL = service_application.config['ATHLETES_XML_URL']
XML_FILE = service_application.config['ATHLETES_XML_FILE']

def get_athletes_xml():
    if not os.path.exists(XML_FILE):
        xml = urllib2.urlopen(XML_URL).read()

        xml_file = open(XML_FILE, 'w')
        xml_file.write(xml)
        xml_file.close()

    return XML_FILE



def athletes_profile_from_xml(logger):
    """
    Vyparsuje profily sportovcov z xml.
    """

    tree = xml.parse(get_athletes_xml())

    root = tree.getroot()

    athletes = []
    for profile in root.findall('profiles/profile'):
        athlete = {}

        athlete['name'] = unicode(profile.find('name').text)
        athlete['img'] = unicode(profile.find('img').text)
        athlete['url'] = unicode(profile.find('url').text)

        athletes.append(athlete)

    return athletes

class FetchListTask(object):

    @inject(session=sqlalchemy.orm.Session, logger=logging.Logger)
    def __init__(self, session, logger):
        self._orm = session
        self._logger = logger

    #TODO: Pouzi service.
    def get_random_clubs(self, count, dim):
        club_count = self._orm.query(SportClub).count()

        clubs = []
        for i in random.sample(xrange(club_count), min(count, club_count)):
            club = self._orm.query(SportClub).order_by(asc(SportClub.id)).limit(1).offset(i).one()
            club = self._orm.query(SportClub).outerjoin(Image).outerjoin(SportClubField).outerjoin(State).outerjoin(Sport).filter(SportClub.id == club.id).one()

            img_url = '#'
            if club.image != None:
                self._logger.debug("Having image {0}.", club.image)
                img_url = url_helper.image(club.image, dim)

            clubs.append({
                'name': club.name,
                'url': url_helper.club(club),
                'img': img_url
            })

        return clubs



    @json_output
    def perform(self, data):
        # TODO: Co ta 2.
        athletes = random.sample(athletes_profile_from_xml(self._logger), 2)

        dim = FetchClubTask.DEFAULT_IMAGE_DIM
        d = data.get_data()
        if 'image_dimension' in d:
            dim = d['image_dimension']

        clubs = []

        return {
            'players': athletes,
            'clubs': self.get_random_clubs(2, dim)
        }
