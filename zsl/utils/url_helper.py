# coding: utf-8
"""
:mod:`zsl.utils.url_helper`
---------------------------

Helper module for URL handling.
"""
from __future__ import unicode_literals
from builtins import str
import unicodedata
import re
import urllib


def slugify(value, allow_unicode=False):
    """Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    :param value: string
    :param allow_unicode: allow utf8 characters
    :type allow_unicode: bool
    :return: slugified string
    :rtype: str

    :Example:
        >>> slugify('pekná líščička')
        'pekna-liscicka'
    """
    value = str(value)

    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
        value = re.sub(r'[^\w\s-]', '', value, flags=re.U).strip().lower()
        return re.sub(r'[-\s]+', '-', value, flags=re.U)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub(r'[^\w\s-]', '', value).strip().lower()
        return re.sub('[-\s]+', '-', value)


def urlencode(query):
    """Encode string to be used in urls (percent encoding).

    :param query: string to be encoded
    :type query: str
    :return: urlencoded string
    :rtype: str

    :Example:
        >>> urlencode('pekná líščička')
        'pekn%C3%A1%20l%C3%AD%C5%A1%C4%8Di%C4%8Dka'
    """
    if hasattr(urllib, 'parse'):
        return urllib.parse.urlencode(query)
    else:
        return urllib.urlencode(query)
