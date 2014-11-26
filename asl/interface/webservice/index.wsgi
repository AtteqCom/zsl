#!/usr/bin/python

# Append the right path to the PYTHONPATH for the CGI script to work.
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

app = None

def get_app(environ):
	if 'ASL_SETTINGS' not in os.environ:
		os.environ['ASL_SETTINGS'] = environ['ASL_SETTINGS']

	if 'APPLICATION_PACKAGE_PATH' not in os.environ:
		os.environ['APPLICATION_PACKAGE_PATH'] = environ['APPLICATION_PACKAGE_PATH']

	from asl.interface import importer
	importer.append_pythonpath()

	# Now import the application and the remaining stuff.
	from asl.application import service_application
	from asl.interface.webservice import web_application_loader

	web_application_loader.load()
	service_application.initialize_dependencies()

	return service_application

# For WSGI.
def application(environ, start_response):
	global app

	if app is None:
		app = get_app(environ)

	return app.wsgi_app(environ, start_response)
