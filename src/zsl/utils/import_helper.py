"""
:mod:`zsl.utils.import_helper`
------------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals

import importlib


def fetch_class(full_class_name):
    """Fetches the given class.

    :param string full_class_name: Name of the class to be fetched.
    """
    (module_name, class_name) = full_class_name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)
