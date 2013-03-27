#!/usr/bin/python

# Append the right path to the PYTHONPATH for the CGI script to work.
import os
import sys
sys.path.append(os.path.abspath('../../'))

# Now import the application and the remaining stuff.
from application import service_application

import interface.webservice.load_app

service_application.initialize_dependencies()


# Run it!
if __name__ == "__main__":
	if len(sys.argv) > 1 and sys.argv[1] == 'shell':
		import bpython
		bpython.embed()

	else:
	    service_application.run()
