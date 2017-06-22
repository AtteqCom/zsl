"""
:mod:`zsl.utils.php_helper`
---------------------------

.. moduleauthor:: Peter Morihladko

Module with functions to help with dealing with code written in PHP.
"""
from __future__ import unicode_literals


def bool_to_str(boolean):
    """Convert ``boolean`` to string like PHP.

    :param boolean: boolean value
    :type boolean: bool
    :return: string representation
    :rtype: str
    """
    return '1' if boolean else ''
