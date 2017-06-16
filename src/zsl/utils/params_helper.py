"""
:mod:`zsl.utils.params_helper`
------------------------------

Helpers for parameter handling

.. moduleauthor:: Peter Morihladko
"""
from __future__ import unicode_literals
from future.utils import viewitems

import inspect
from functools import reduce


class RequestException(Exception):
    """Exception raised on bad request"""
    pass


def required_params(data, *r_params):
    """Check if given parameters are in the given dict, if not raise an
    exception.

    :param data: data to check
    :type data: dict
    :param r_params: required parameters
    :raises RequestException: if params not in data
    """

    if not reduce(lambda still_valid, param: still_valid and param in data,
                  r_params, True):
        raise RequestException(msg_err_missing_params(*r_params))


def msg_err_missing_params(*params):
    return "Missing one or more required parameters (%s)" % '|'.join(params)


def safe_args(fn, args):
    """Check if ``args`` as a dictionary has the required parameters of ``fn``
    function and filter any waste parameters so ``fn`` can be safely called
    with them.

    :param fn: function object
    :type fn: Callable
    :param args: dictionary of parameters
    :type args: dict
    :return: dictionary to be used as named params for the ``fn``
    :rtype: dict
    """
    fn_args = inspect.getargspec(fn)

    if fn_args.defaults:
        required_params(args, fn_args.args[:-len(fn_args.defaults)])
    else:
        required_params(args, fn_args)

    if not fn_args.keywords:
        return {key: value for key, value in viewitems(args) if key in fn_args.args}
    else:
        return args
