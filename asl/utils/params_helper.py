"""
Helpers for parameter handling

.. moduleauthor:: Peter Morihladko
"""

import inspect


class RequestException(Exception):
    pass


def required_params(data, *r_params):
    """
    Check if given parameters are in the given dict, if not raise
    an exception

    :param data: data to check
    :type data: dict
    :param required_params: required parameters
    :raise RequestException: if params not in data
    """

    if not reduce(lambda still_valid, param: still_valid and param in data,
                  r_params, True):
        raise RequestException(msg_err_missing_params(*r_params))


def msg_err_missing_params(*params):
    return "Missing one or more required parameters (%s)" % '|'.join(params)


def safe_args(fn, args):
    """
    Check if ``args`` as a dictionary has the required parameters of
    ``fn`` function and filter any waste parameters so ``fn`` can be
    safely called with them

    :param fn: function object
    :type fn: callable
    :param args: dictionary of parameters
    :type args: dict
    :return: dictionary to be used as named params for the ``fn``
    :rtype: dict
    '"""
    fn_args = inspect.getargspec(fn)

    if fn_args.defaults:
        required_params(args, fn_args.args[:-len(fn_args.defaults)])
    else:
        required_params(args, fn_args)

    if not fn_args.keywords:
        return dict((key, value) for key, value in args.iteritems() if key in fn_args.args)
    else:
        return args