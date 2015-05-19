'''
Created on 17.3.2015

@author: Martin Babka
'''

from importer import initialize_cli_application
initialize_cli_application()


import importlib
import unittest
from asl.application.service_application import service_application

# Set up unit test mode.
from asl.router.method import identity_responder, set_default_responder
set_default_responder(identity_responder)

# Set up necessities.
test_module = importlib.import_module(service_application.config['TEST_PACKAGE'])


# Run it!
def main():
    unittest.main(module=test_module)

if __name__ == "__main__":
    main()
