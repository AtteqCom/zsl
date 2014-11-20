# Now import the application and the remaining stuff.
from asl.application import service_application

def load_testers():
    # TODO: A better configuration.
    __import__('asl.interface.webservice.resource_tester')
    __import__('asl.interface.webservice.web_task_tester')

def load():
    load_testers()

# Shortcut
app = service_application

# Do the mapping.
@app.route("/", defaults={'path': ''}, methods=("POST", "GET"))
@app.route("/<path:path>", methods=("POST", "GET"))
def mapping(path):
    response_str = "Default handler, not found! Path not found '{0}'.".format(path);
    app.logger.warn(response_str)
    return response_str, 404
