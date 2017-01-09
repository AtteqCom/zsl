#!/usr/bin/python

from past.builtins import execfile
import os

app = None


# Application preparation.
def get_app(environ):
    if 'ASL_SETTINGS' not in os.environ:
        os.environ['ASL_SETTINGS'] = environ['ASL_SETTINGS']

    if 'APPLICATION_PACKAGE_PATH' not in os.environ:
        os.environ['APPLICATION_PACKAGE_PATH'] = environ['APPLICATION_PACKAGE_PATH']

    # For Apache mod_wsgi convenience.
    if 'ASL_IMPORT_SCRIPT' in environ and 'ASL_IMPORT_SCRIPT' not in os.environ:
        os.environ['ASL_IMPORT_SCRIPT'] = environ['ASL_IMPORT_SCRIPT']
    if 'ASL_IMPORT_SCRIPT' in os.environ:
        execfile(os.environ['ASL_IMPORT_SCRIPT'])

    execfile(os.path.dirname(__file__) + '/importer.py')

    from zsl.interface.importer import initialize_web_application
    initialize_web_application()
    from zsl.application.service_application import service_application
    return service_application


# For WSGI.
def application(environ, start_response):
    global app

    if app is None:
        app = get_app(environ)

    return app.wsgi_app(environ, start_response)