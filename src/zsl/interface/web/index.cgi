#!/usr/bin/python

from zsl import Zsl
from zsl.application.containers.web_container import WebContainer

# Run it!
if __name__ == "__main__":
	service_application = Zsl(__name__, modules=WebContainer.modules())

	from wsgiref.handlers import CGIHandler
	CGIHandler().run(app)
