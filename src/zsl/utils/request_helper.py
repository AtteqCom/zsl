"""
:mod:`zsl.utils.request_helper`

Helper module for working with request.

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals

from future.utils import viewitems


def args_to_dict(args):
    """Converts request arguments to a simple dictionary. Uses only the first
    value.

    :param args: flask's request args object
    :type args: request.args
    :return: a simple dict from args
    :rtype: dict
    """
    return args.to_dict(flat=True)
