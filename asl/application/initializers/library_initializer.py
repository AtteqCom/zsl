'''
Created on 27.2.2015

@author: Martin Babka
'''
import logging
from flask import Config
from asl.application.initializers import injection_module
import sys
from asl.vendor import append_paths

class LibraryInitializer:

    def initialize(self, binder):
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
