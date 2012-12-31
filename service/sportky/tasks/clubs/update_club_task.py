from task.task_decorator import json_input, json_output
from injector import inject
import sqlalchemy.orm
from db.models.raw import SportClub
import logging
from datetime import datetime
from db.models.validators import SportClubForm
from werkzeug.datastructures import MultiDict

class UpdateClubTask(object):

    @inject(session=sqlalchemy.orm.Session, logger=logging.Logger)
    def __init__(self, session, logger):
        self.__orm = session
        self.__logger = logger

    @json_input
    @json_output
    def perform(self, data):
        try:
            club_data = data.get_data()['club']

            f = SportClubForm(MultiDict(club_data))
            if not f.validate():
                return {"result": False, "errors": f.errors}

            try:
                club_data['created'] = datetime.strptime(club_data['created'], "%d. %m. %Y")
            except Exception:
                pass
            club_db = self.__orm.query(SportClub).filter(SportClub.id == club_data['id']).one()

            for k in club_db.__dict__.keys():
                if k in club_data:
                    setattr(club_db, k, club_data[k])

            club_db.update_url()
            self.__orm.commit()

            res = True
        except Exception as e:
            print e
            res = False

        return {"result": res}
