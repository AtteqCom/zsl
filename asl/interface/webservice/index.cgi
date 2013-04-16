#!/usr/bin/python

# Append the right path to the PYTHONPATH for the CGI script to work.
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from asl.interface import importer
importer.append_pythonpath()

# Now import the application and the remaining stuff.
from asl.application import service_application
from asl.interface.webservice import web_application_loader

# Load and init the application.
web_application_loader.load()
service_application.initialize_dependencies()

# Run it!
if __name__ == "__main__":
	from wsgiref.handlers import CGIHandler
	CGIHandler().run(service_application)
