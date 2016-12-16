"""
:mod:`asl.utils.php_helper`

.. moduleauthor:: Peter Morihladko

Some handy function when dealing with code written in PHP
"""
from __future__ import unicode_literals


def bool_to_str(boolean):
    """
    Convert ``boolean`` to string like PHP
    """
    return '1' if boolean else ''
