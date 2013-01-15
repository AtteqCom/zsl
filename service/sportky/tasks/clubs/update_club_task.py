from task.task_decorator import json_input, json_output
from injector import inject
import sqlalchemy.orm
from db.models.raw import SportClub, SportClubField
import logging
from datetime import datetime
from db.models.validators import SportClubForm
from werkzeug.datastructures import MultiDict
from application import service_application

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

            app = service_application
            app.logger.debug("Update club task with data '{0}'.".format(club_data))

            f = SportClubForm(MultiDict(club_data))
            if not f.validate():
                return {"result": False, "errors": f.errors}

            try:
                club_data['created'] = datetime.strptime(club_data['created'], "%d. %m. %Y")
            except Exception:
                pass
            club_db = self.__orm.query(SportClub).outerjoin(SportClubField).filter(SportClub.id == club_data['id']).one()

            for k in club_db.__dict__.keys():
                if k in club_data and k != "sport_club_fields":
                    app.logger.debug("Setting property {0}.".format(k));
                    setattr(club_db, k, club_data[k])

            data_fields = {}
            for f in club_data['sport_club_fields']:
                if f['id']:
                    data_fields[int(f['id'])] = f

            app.logger.debug("Update club fields '{0}'.".format(data_fields))

            club_db.update_url()
            self.__orm.commit()

            res = True
        except Exception as e:
            app.logger.error(e)
            res = False

        return {"result": res}
