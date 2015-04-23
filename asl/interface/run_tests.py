'''
Created on 17.3.2015

@author: Martin Babka
'''
import sys
import os
import importlib
import unittest

# Initialize
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'));
from asl.application import service_application
service_application.initialize_dependencies()

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
