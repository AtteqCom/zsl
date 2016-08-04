'''
:mod:`asl.utils.string_helper`

.. moduleauthor:: Martin Babka
'''
import re
import random
import string

_html_tag_re = re.compile(ur'''</?\w+((\s+\w+(\s*=\s*(?:".*?"|'.*?'|[^'">\s]+))?)+\s*|\s*)/?>''', flags=re.IGNORECASE)
_html_tag_re_un = re.compile(
    ur'''</?\w+((\s+\w+(\s*=\s*(?:".*?"|'.*?'|[^'">\s]+))?)+\s*|\s*)/?>''', flags=re.IGNORECASE | re.UNICODE)


def underscore_to_camelcase(value):
    def camelcase():
        while True:
            yield str.capitalize

    value = str(value)
    c = camelcase()
    return "".join(c.next()(x) if x else '_' for x in value.split("_"))


def camelcase_to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def et_node_to_string(et_node, default=u''):
    '''
    @et_node: Element
    '''

    return unicode(et_node.text).strip() if et_node is not None and et_node.text else default


def generate_random_string(size=6, chars=string.ascii_uppercase + string.digits):
    '''
    Random string generator.

    @param size: Length of the returned string.
    @param chars: List of the usable characters.
    @return: The random string.
    '''
    return ''.join(random.choice(chars) for _ in range(size))


def addslashes(s, l=["\\", "'", ]):
    # l = ["\\", '"', "'", "\0", ]
    for i in l:
        if i in s:
            s = s.replace(i, '\\' + i)
    return s


def xstr(s):
    '''
    If ``s`` is None return empty string
    '''
    return '' if s is None else str(s)


def xunicode(s):
    '''
    If ``s`` is None return empty string
    '''
    return '' if s is None else unicode(s)


def strip_html_tags(s):
    '''
    Remove all html tags from string
    '''
    return _html_tag_re.sub('', s)


def strip_html_tags_unicode(s):
    '''
    Remove all html tags from unicode string
    '''
    return _html_tag_re_un.sub(u'', s)
