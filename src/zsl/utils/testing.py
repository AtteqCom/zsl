"""
:mod:`zsl.utils.testing`
------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals
from __future__ import absolute_import

import importlib
import unittest

from zsl import inject, Config
from zsl.router.method import identity_responder, set_default_responder


_test_responder_set = False


def set_test_responder():
    global _test_responder_set
    if _test_responder_set:
        return
    _test_responder_set = True
    set_default_responder(identity_responder)


@inject(config=Config)
def load_and_run_tests(config):
    """Load application test package and run it using testing util.

    :param config: application configuration, injected
    :type config: Config
    """
    set_test_responder()

    test_module = importlib.import_module(config['TEST_PACKAGE'])

    unittest.main(module=test_module)
