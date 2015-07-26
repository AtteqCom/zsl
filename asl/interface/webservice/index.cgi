#!/usr/bin/python

from asl.interface.importer import initialize_web_application
initialize_web_application()

# Now import the application and the remaining stuff.
from asl.application import service_application

# Run it!
if __name__ == "__main__":
	from wsgiref.handlers import CGIHandler
	CGIHandler().run(service_application)
