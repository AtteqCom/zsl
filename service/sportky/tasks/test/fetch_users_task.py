from task.task_decorator import json_output
from injector import inject
from application.service_application import SportkyFlask
import sqlite3;


class FetchUsersTask(object):
    @inject(app=SportkyFlask)
    def __init__(self, app):
        self._app = app
        self._db = sqlite3.connect('/tmp/test.users.db')
        self._db.row_factory = sqlite3.Row
        
        return self

    @json_output
    def perform(self, data):
        users = self._db.execute('SELECT * FROM `user` ORDER BY `id`').fetchall()
        
        return map(lambda x: dict(x),users)