"""
:mod:`zsl.utils.request_helper`

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals
from future.utils import viewitems


def args_to_dict(args):
    """
    Converts request arguments to a simple dictionary. Uses only the first value.
    """
    return {key: value[0] for key, value in viewitems(args)}
