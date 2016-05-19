'''
:mod:`asl.utils.url_helper`

.. moduleauthor:: Peter Morihladko
'''
import unicodedata
import re

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    Drsny copy-paste z Djanga
    """
    if isinstance(value, str):
	try:
	    value = unicode(value)
	except UnicodeDecodeError:
	    value = unicode(value, 'utf-8')
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)
