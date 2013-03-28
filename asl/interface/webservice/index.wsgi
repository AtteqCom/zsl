#!/usr/bin/python

# Append the right path to the PYTHONPATH for the CGI script to work.
import sys
from asl.interface import importer
importer.append_pythonpath()

# Now import the application and the remaining stuff.
from asl.application import service_application
from wsgiref.handlers import CGIHandler

from asl.interface.webservice import web_application_loader
web_application_loader.load()

# For WSGI.
application = service_application
service_application.initialize_dependencies()
