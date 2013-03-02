from injector import inject
from application.service_application import SportkyFlask
from task import task_status
import sqlite3

class User(object):
	
	@inject(app=SportkyFlask)
	def __init__(self, db, app):
		self._app = app
		self._db = sqlite3.connect('/tmp/test.users.db')
		self._db.row_factory = sqlite3.Row
		
		return self
	
	def create(self, param, data):
		try:
			with self._db:
				if self._db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'").fetchone() is None:
					self._db.execute("CREATE TABLE `user` (name text, surname text)")
					
				id = self._db.execute("INSERT INTO user (name, surname) VALUES (:name, :surname)", data).lastrowid
				
			return dict(
				{'id': id}, 
				**task_status.OK
			)
			
		except:
			return task_status.ERROR
		

	def read(self, param, data=None):
		id = param
			
		user = self._db.execute("SELECT *id FROM user WHERE id = ?", str(id)).fetchone()
		
		return dict(user)
		
	def update(self, param, data):
		try:
			with self._db:
				self._db.execute("UPDATE user SET name = :name, surname = :surname WHERE id = :id", data)
			
			return task_status.OK
		except:
			return task_status.ERROR
	
	def delete(self, param, data=None):
		try:
			with self._db:
				self._db.execute("DELETE FROM user WHERE id = ?", str(param))
			
			return task_status.OK
		except:
			return task_status.ERROR


