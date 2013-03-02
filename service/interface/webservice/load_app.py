# Now import the application and the remaining stuff.
from application import service_application

import interface.webservice.resource_tester
import interface.webservice.web_task_tester

# Shortcut
app = service_application

# Do the mapping.
@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def mapping(path):
    app.logger.debug("Hello wording!")
    return "Hello World! Using path '{0}'.".format(path)
