#!/usr/bin/python

import os
from asl.interface.importer import initialize_web_application

app = None

# Application preparation.
def get_app(environ):
	if 'ASL_SETTINGS' not in os.environ:
		os.environ['ASL_SETTINGS'] = environ['ASL_SETTINGS']

	if 'APPLICATION_PACKAGE_PATH' not in os.environ:
		os.environ['APPLICATION_PACKAGE_PATH'] = environ['APPLICATION_PACKAGE_PATH']

	initialize_web_application()
	return service_application

# For WSGI.
def application(environ, start_response):
	global app

	if app is None:
		app = get_app(environ)

	return app.wsgi_app(environ, start_response)
