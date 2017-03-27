"""
:mod:`zsl.interface.run_tests`
------------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals

from zsl.router.method import identity_responder, set_default_responder
import importlib
import unittest

_test_responder_set = False


def set_test_responder():
    global _test_responder_set
    if _test_responder_set:
        return
    _test_responder_set = True
    set_default_responder(identity_responder)

# Set up unit test mode.
set_test_responder()

# Set up necessities.
test_module = importlib.import_module(service_application.config['TEST_PACKAGE'])


# Run it!
def main():
    unittest.main(module=test_module)

if __name__ == "__main__":
    main()
