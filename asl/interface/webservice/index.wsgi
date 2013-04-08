#!/usr/bin/python

# Append the right path to the PYTHONPATH for the CGI script to work.
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

# For WSGI.
def application(environ, start_response):
	os.environ['ASL_SETTINGS'] = environ['ASL_SETTINGS']
	os.environ['APPLICATION_PACKAGE_PATH'] = environ['APPLICATION_PACKAGE_PATH']

	from asl.interface import importer
	importer.append_pythonpath()

	# Now import the application and the remaining stuff.
	from asl.application import service_application
	from wsgiref.handlers import CGIHandler

	from asl.interface.webservice import web_application_loader
	web_application_loader.load()

	service_application.initialize_dependencies()
	service_application.wsgi_app(environ, start_response)
