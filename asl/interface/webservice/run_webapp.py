#!/usr/bin/python

# Append the right path to the PYTHONPATH for the CGI script to work.

import sys
from asl.interface.importer import append_pythonpath
append_pythonpath()
from asl.interface.webservice import web_application_loader
web_application_loader.load()

# Now import the application and the remaining stuff.
from asl.application import service_application
service_application.initialize_dependencies()

# Run it!
if __name__ == "__main__":
	if len(sys.argv) > 1 and sys.argv[1] == 'shell':
		import bpython
		bpython.embed()
	else:
		service_application.run()
