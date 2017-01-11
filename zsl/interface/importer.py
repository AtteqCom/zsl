"""
:mod:`asl.interface.importer`

The modules deals with the initialization of the basics - python path and then loads and initializes the application
if necessary.

.. moduleauthor:: Martin Babka
"""

import os
import sys


class InitializationContext(object):

    def __init__(self, unit_test):
        self._unit_test = unit_test

    def get_unit_testing(self):
        return self._unit_test
    unit_testing = property(get_unit_testing)


def _append_application_pythonpath():
    """
    Appends application to python path.
    """
    app_package_path = os.environ.get('APPLICATION_PACKAGE_PATH')

    if app_package_path is None:
        raise Exception("Application path is not set. Set it using the APPLICATION_PACKAGE_PATH environment variable.")

    sys.path.append(app_package_path)


def _append_pythonpath():
    """
    Appends required paths to python path. Actually adds the application to python path.
    """
    _append_application_pythonpath()

_skip_appending_asl_path = False


def _append_asl_path_to_pythonpath():
    global _skip_appending_asl_path
    if _skip_appending_asl_path:
        return

    # TODO: Consider removing automatic path initialization!
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    # TODO: This is because of settings.default_settings import in application object.
    # This should be somehow more inteligent or related to APPLICATION_PACKAGE_PATH.
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

    # Remove the path which could collide with the main libraries.
    to_remove = []
    for pa in sys.path:
        if os.path.abspath(pa) == os.path.abspath(os.path.dirname(__file__)):
            to_remove.append(pa)
    for pa in to_remove:
        sys.path.remove(pa)


def skip_appending_asl_path_to_pythonpath():
    global _skip_appending_asl_path
    _skip_appending_asl_path = True


def _initialize_environment():
    for x in ['env.py', os.path.join(os.path.dirname(__file__), '..', '..', '..', 'env.py')]:
        try:
            execfile(x)
        except:
            pass


def initialize_service_application(ctx):
    from zsl.application.service_application import service_application as app
    app.initialize_dependencies(ctx)

_cli_application_initialized = False


def initialize_cli_application(ctx):
    global _cli_application_initialized
    if _cli_application_initialized:
        return
    _cli_application_initialized = True

    _initialize_environment()
    _append_pythonpath()
    _append_asl_path_to_pythonpath()
    initialize_service_application(ctx)


def is_initialized():
    return _cli_application_initialized

_web_application_initialized = False


def initialize_web_application():
    global _web_application_initialized
    ctx = InitializationContext(unit_test=False)
    if _web_application_initialized:
        return
    _web_application_initialized = True

    initialize_cli_application(ctx)
    from zsl.interface.webservice import web_application_loader
    web_application_loader.load()
