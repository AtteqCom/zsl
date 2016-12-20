"""
:mod:`zsl.utils.url_helper`

.. moduleauthor:: Peter Morihladko
"""
from __future__ import unicode_literals
from builtins import str
import unicodedata
import re
import urllib


def slugify(value, allow_unicode=False):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
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
    if hasattr(urllib, 'parse'):
        return urllib.parse.urlencode(query)
    else:
        return urllib.urlencode(query)
