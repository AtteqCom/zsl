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


class LibraryInitializer(object):
    # TODO: Change to iface

    """Add vendor modules to current path."""
    @staticmethod
    @inject
    def initialize(config: Config) -> None:
        logging.debug("Initializing project external libraries.")

        external_libraries = config.get('EXTERNAL_LIBRARIES', None)
        if external_libraries is None:
            return

        vendor_path = external_libraries['vendor_path']
        append_paths(vendor_path, external_libraries['libs'])

        logging.info("Current PYTHON_PATH={0}.".format(sys.path))
        logging.debug("Project external libraries initialized.")
