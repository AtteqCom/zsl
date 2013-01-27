from task.task_decorator import json_input, json_output
from injector import inject
from datetime import datetime
from db.models.validators import SportClubForm
from werkzeug.datastructures import MultiDict
from db.models.raw.model_helper import ModelHelper
from application.service_application import SportkyFlask
from sportky.service.club_service import ClubService
from db.models.raw import SportClubField

class UpdateClubTask(object):

    @inject(app=SportkyFlask, club_service=ClubService)
    def __init__(self, app, club_service):
        self._app = app
        self._club_service = club_service

    @json_input
    @json_output
    def perform(self, data):
        try:
            self._app.logger.debug("Updating club.")
            club_data = data.get_data()['club']

            f = SportClubForm(MultiDict(club_data))
            self._app.logger.info("Club: {0}.".format(club_data))
            if not f.validate():
                self._app.logger.info("Validation failed.");
                return {"result": False, "errors": f.errors}

            try:
                club_data['created'] = datetime.strptime(club_data['created'], "%d. %m. %Y")
            except Exception:
                pass

            club_db = self._club_service.fetch(club_data['id'])
            ModelHelper.update_model(club_db, club_data, ["sport_club_fields"])

            # TODO: As a general helper.
            data_fields = {}
            new = []
            for f in club_data['sport_club_fields']:
                if f['id']:
                    self._app.logger.debug("Updating field {0}.".format(f['id']))
                    data_fields[int(f['id'])] = f
                else:
                    self._app.logger.debug("New field created {0}.".format(f['name']))
                    scf = SportClubField()
                    scf.sport_club_id = club_db.id
                    scf.update(f, [], True)
                    new.append(scf)

            db_fields = club_db.sport_club_fields
            to_remove = []
            for f in db_fields:
                fid = int(f.id)
                if not fid in data_fields:
                    if fid:
                        self._app.logger.debug("Deleting field {0}.".format(fid))
                        to_remove.append(f)
                else:
                    self._app.logger.debug("Updating field {0} to raw model.".format(fid))
                    f.update(data_fields[fid])

            def remove_old_fields():
                for f in to_remove:
                    self._club_service.delete_sport_club_field(f)

            for f in new:
                club_db.sport_club_fields.append(f)

            self._club_service.append_transaction_callback(remove_old_fields)
            self._club_service.save(club_db)

            res = True
        except Exception as e:
            self._app.logger.error(e)
            res = False

        return {"result": res}
