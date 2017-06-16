"""
:mod:`zsl.utils.string_helper`
------------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals
from builtins import str
from builtins import range
import re
import random
import string

_html_tag_re = re.compile(r'''</?\w+((\s+\w+(\s*=\s*(?:".*?"|'.*?'|[^'">\s]+))?)+\s*|\s*)/?>''', flags=re.IGNORECASE)
_html_tag_re_un = re.compile(
    r'''</?\w+((\s+\w+(\s*=\s*(?:".*?"|'.*?'|[^'">\s]+))?)+\s*|\s*)/?>''', flags=re.IGNORECASE | re.UNICODE)


def underscore_to_camelcase(value, first_upper=True):
    """Transform string from underscore_string to camelCase.

    :param value: string with underscores
    :param first_upper: the result will have its first character in upper case
    :type value: str
    :return: string in CamelCase or camelCase according to the first_upper
    :rtype: str

    :Example:
        >>> underscore_to_camelcase('camel_case')
        'CamelCase'
        >>> underscore_to_camelcase('camel_case', False)
        'camelCase'
    """
    value = str(value)
    camelized = "".join(x.title() if x else '_' for x in value.split("_"))
    if not first_upper:
        camelized = camelized[0].lower() + camelized[1:]
    return camelized


def camelcase_to_underscore(name):
    """Transform string from camelCase to underscore_string.

    :param name: string in camelcase
    :type name: str
    :return: string with underscores
    :rtype: str

    :Example:
        >>> camelcase_to_underscore('camelCase')
        'camel_case'
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def et_node_to_string(et_node, default=''):
    """Simple method to get stripped text from node or ``default`` string if None is given.

    :param et_node: Element or None
    :param default: string returned if None is given, default ``''``
    :type et_node: xml.etree.ElementTree.Element, None
    :type default: str
    :return: text from node or default
    :rtype: str
    """

    return str(et_node.text).strip() if et_node is not None and et_node.text else default


def generate_random_string(size=6, chars=string.ascii_uppercase + string.digits):
    """Generate random string.

    :param size: Length of the returned string. Default is 6.
    :param chars: List of the usable characters. Default is string.ascii_uppercase + string.digits.
    :type size: int
    :type chars: str
    :return: The random string.
    :rtype: str
    """
    return ''.join(random.choice(chars) for _ in range(size))


def addslashes(s, l=None):
    """Add slashes for given characters. Default is for ``\`` and ``'``.

    :param s: string
    :param l: list of characters to prefix with a slash ``\``
    :return: string with slashed characters
    :rtype: str

    :Example:
        >>> addslashes("'")
        "\\'"
    """
    if l is None:
        l = ["\\", "'", ]

    # l = ["\\", '"', "'", "\0", ]
    for i in l:
        if i in s:
            s = s.replace(i, '\\' + i)
    return s


def xstr(s):
    """If ``s`` is None return empty string.

    :param s: string
    :return: s or an empty string if s is None
    :rtype: str

    :Example:
        >>> xstr(None)
        ''
    """
    return '' if s is None else str(s)


def xunicode(s):
    """If ``s`` is None return empty string

    .. deprecated::
       Use :func:`xstr` instead.

    :param s: string
    :return: s or an empty string if s in None
    :rtype: str
    """
    return '' if s is None else str(s)


def strip_html_tags(s):
    """Remove all html tags from string.

    :param s: string
    :type s: str
    :return: string with stripped html tags
    :rtype: str

    :Example:
        >>> strip_html_tags('<h1>hello <i>world</i></h1>')
        'hello world'
    """
    return _html_tag_re.sub('', s)


def strip_html_tags_unicode(s):
    """Remove all html tags from string.

    .. deprecated::
       Use :func:`strip_html_tags` instead.

    :param s: string
    :type s: str
    :return: string with stripped html tags
    :rtype: str
    """
    return _html_tag_re_un.sub('', s)
