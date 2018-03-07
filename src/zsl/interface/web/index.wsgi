#!/usr/bin/python

import os

from past.builtins import execfile

app = None


# Application preparation.
def get_app(environ):
    if 'SETTINGS' not in os.environ:
        os.environ['SETTINGS'] = environ['SETTINGS']

    # For Apache mod_wsgi convenience.
    if 'ASL_IMPORT_SCRIPT' in environ and 'ASL_IMPORT_SCRIPT' not in os.environ:
        os.environ['ASL_IMPORT_SCRIPT'] = environ['ASL_IMPORT_SCRIPT']
    if 'ASL_IMPORT_SCRIPT' in os.environ:
        execfile(os.environ['ASL_IMPORT_SCRIPT'])

    from zsl import Zsl
    from zsl.application.containers.web_container import WebContainer

    service_application = Zsl(__name__, modules=WebContainer.modules())
    return service_application


# For WSGI.
def application(environ, start_response):
    global app

    if app is None:
        app = get_app(environ)

    return app.wsgi_app(environ, start_response)
