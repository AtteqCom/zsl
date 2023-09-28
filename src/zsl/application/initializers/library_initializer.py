"""
:mod:`zsl.application.initializers.library_initializer`
-------------------------------------------------------
"""
import logging
import os
import sys

from zsl import Config, inject


def append_paths(path, vendor_modules):
    new_path = []
    for v in vendor_modules:
        new_path.append(path + os.sep + v)
    sys.path = new_path + sys.path


class LibraryInitializer:
    """Add vendor modules to current path."""
    @staticmethod
    @inject(config=Config)
    def initialize(config):
        logging.debug("Initializing project external libraries.")

        external_libraries = config.get('EXTERNAL_LIBRARIES', None)
        if external_libraries is None:
            return

        vendor_path = external_libraries['vendor_path']
        append_paths(vendor_path, external_libraries['libs'])

        logging.info("Current PYTHON_PATH={0}.".format(sys.path))
        logging.debug("Project external libraries initialized.")
