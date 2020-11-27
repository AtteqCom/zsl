"""
:mod:`zsl.utils.request_helper`

Helper module for working with request.

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals

from future.utils import viewitems


def args_to_dict(args):
    """Converts request arguments to a simple dictionary. If an argument
    appears multiple times, the resulting dictionary will contain list
    of all of its values.

    :param args: flask's request args object
    :type args: request.args
    :return: a simple dict from args
    :rtype: dict
    """
    args_dict = {}
    for param_name, param_value in args.items(multi=True):
        if param_name not in args_dict:
            args_dict[param_name] = param_value
        elif not isinstance(args_dict[param_name], list):
            current_value = args_dict[param_name]
            args_dict[param_name] = [current_value, param_value]
        else:
            args_dict[param_name].append(param_value)

    return args_dict
