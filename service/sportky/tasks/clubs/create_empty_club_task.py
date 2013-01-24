from task.task_decorator import json_input, json_output
from injector import inject
from db.models.raw import SportClub
from datetime import datetime
from sportky.service.club_service import ClubService
from application.service_application import SportkyFlask

class CreateEmptyClubTask(object):

    @inject(club_service=ClubService, app=SportkyFlask)
    def __init__(self, club_service, app):
        self._app = app
        self._club_service = club_service

    @json_input
    @json_output
    def perform(self, data):
        c = SportClub()
        c.added = datetime.now()
        c.active = False
        c.flag_created_year = False
        c.city = ''
        c.coach = ''
        c.current_squad = False
        c.homepage = ''
        c.league = ''
        c.name = ''
        c.president = ''
        c.stadium = ''
        c.magazine_id = data.get_data()['magazine_id']
        c.url = ''
        self._club_service.save(c)
        return { 'id': c.id }
