"""
:mod:`zsl.utils.type_helper`
----------------------------

Helper module for handling types.

.. moduleauthor:: peter
"""
from __future__ import unicode_literals


def not_empty_list(l):
    """Check if given value is a non-empty list.

    :param l: value
    :return: True on non-empty list, False otherwise
    :rtype: bool

    :Example:
        >>> not_empty_list([1, 2, 3])
        True
        >>> not_empty_list(None)
        False
    """
    return isinstance(l, list) and len(l) > 0
