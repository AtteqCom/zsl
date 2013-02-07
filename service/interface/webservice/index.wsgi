#!/usr/bin/python

# Append the right path to the PYTHONPATH for the CGI script to work.
import os
import sys

# Now import the application and the remaining stuff.
from application import service_application
from wsgiref.handlers import CGIHandler

import interface.webservice.web_task_tester

# Shortcut
app = service_application

# Do the mapping.
@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def mapping(path):
    app.logger.debug("Hello wording!")
    return "Hello World! Using path '{0}'.".format(path)

# For WSGI.
application = app
app.initialize_dependencies()
