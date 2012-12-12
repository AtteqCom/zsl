#!/usr/bin/python

# Append the right path to the PYTHONPATH for the CGI script to work.
import os
import sys
sys.path.append(os.path.abspath('../../'))

# Now import the application and the remaining stuff.
from application import service_application
from wsgiref.handlers import CGIHandler

# Shortcut
app = service_application

# Do the mapping.
@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def mapping(path):
    return "Hello World! Using path '{0}' and {1}.".format(path, app.config['BLAA']);

# Run it!.
if __name__ == "__main__":
    CGIHandler().run(app)