from task.task_decorator import json_input, json_output
from injector import inject
import sqlalchemy.orm
from db.models.raw import SportClub, SportClubField
import logging
from datetime import datetime
from db.models.validators import SportClubForm
from werkzeug.datastructures import MultiDict
from db.models.raw.model_helper import ModelHelper

class UpdateClubTask(object):

    @inject(session=sqlalchemy.orm.Session, logger=logging.Logger)
    def __init__(self, session, logger):
        self.__orm = session
        self.__logger = logger

    @json_input
    @json_output
    def perform(self, data):
        try:
            self.__logger.debug("Updating club.")
            club_data = data.get_data()['club']

            f = SportClubForm(MultiDict(club_data))
            if not f.validate():
                return {"result": False, "errors": f.errors}

            try:
                club_data['created'] = datetime.strptime(club_data['created'], "%d. %m. %Y")
            except Exception:
                pass
            club_db = self.__orm.query(SportClub).outerjoin(SportClubField).filter(SportClub.id == club_data['id']).one()

            ModelHelper.update_model(club_db, club_data, ["sport_club_fields"])

            # TODO: As a general helper.
            data_fields = {}
            new = []
            for f in club_data['sport_club_fields']:
                if f['id']:
                    self.__logger.debug("Updating field {0}.".format(f['id']))
                    data_fields[int(f['id'])] = f
                else:
                    self.__logger.debug("New field created {0}.".format(f['name']))
                    scf = SportClubField()
                    scf.sport_club_id = club_db.id
                    scf.update(f, [], True)
                    new.append(scf)

            db_fields = club_db.sport_club_fields
            for f in db_fields:
                fid = int(f.id)
                if not fid in data_fields:
                    if fid:
                        self.__logger.debug("Deleting field {0}.".format(fid))
                        self.__orm.delete(f)
                else:
                    self.__logger.debug("Updating field {0} to raw model.".format(fid))
                    f.update(data_fields[fid])

            for f in new:
                self.__orm.add(f)

            club_db.update_url()
            self.__orm.commit()

            res = True
        except Exception as e:
            self.__logger.error(e)
            res = False

        return {"result": res}
