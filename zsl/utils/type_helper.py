"""
:mod:`asl.utils.type_helper`

.. moduleauthor:: peter
"""
from __future__ import unicode_literals


def not_empty_list(l):
    return isinstance(l, list) and len(l) > 0
