# Now import the application and the remaining stuff.
from application import service_application

def load_testers():
    # TODO: A better configuration.
    __import__('interface.webservice.resource_tester')
    __import__('interface.webservice.web_task_tester')

def load():
    load_testers()

# Shortcut
app = service_application

# Do the mapping.
@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def mapping(path):
    app.logger.debug("Hello wording!")
    return "Hello World! Using path '{0}'.".format(path)
