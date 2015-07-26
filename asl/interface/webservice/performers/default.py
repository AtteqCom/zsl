'''
:mod:`asl.interface.webservice.performers.default`

.. moduleauthor:: Martin Babka
'''
from asl.application.service_application import service_application

# Shortcut
app = service_application

# Do the mapping.
@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def not_found_mapping(path):
    '''
    Default web request handler. Only returns 404 status code.
    '''
    
    response_str = "Default handler, not found! Path not found '{0}'.".format(path);
    app.logger.warn(response_str)
    return response_str, 404
