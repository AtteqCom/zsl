# -*- coding: utf-8 -*-
"""
:mod:`zsl.utils.date_helper`
----------------------------
"""
from __future__ import unicode_literals

from builtins import *


def documentation_link(chapter):
    # type: (str)->str
    """
    Creates a link to the documentation.

    This method is useful for showing a link to the ZSL documentation in case of any misconfiguration, etc.
    :param chapter: Chapter name in to which the link points. Use underscores instead of spaces.
    :return: The absolute link to the documentation.
    """
    return "http://zsl.readthedocs.io/en/latest/{0}.html".format(chapter)
