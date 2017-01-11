import logging
import sys
import os

from flask import Config
from zsl.application.initializers import injection_module


def append_paths(path, vendor_modules):
    new_path = []
    for v in vendor_modules:
        new_path.append(path + os.sep + v)
    sys.path = new_path + sys.path


class LibraryInitializer(object):
    @staticmethod
    def initialize(binder):
        logger = binder.injector.get(logging.Logger)
        logger.debug("Initializing project external libraries.")
        config = binder.injector.get(Config)

        external_libraries = config.get('EXTERNAL_LIBRARIES', None)
        if external_libraries is None:
            return

        vendor_path = external_libraries['vendor_path']
        append_paths(vendor_path, external_libraries['libs'])

        logger.info("Current PYTHON_PATH={0}.".format(sys.path))
        logger.debug("Project external libraries initialized.")


@injection_module
def application_initializer_module(binder):
    LibraryInitializer().initialize(binder)
