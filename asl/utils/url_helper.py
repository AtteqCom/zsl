'''
Created on 21.01.2013

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
        value = unicode(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)


def club(club):
    return '/sportove-kluby/{id}/{name}'.format(id=club.id, name=slugify(club.name))

def image(image, dim):
    return '/cacheImg/obr/{0}px/{1}-{2}.{3}'.format(dim, slugify(image.description), image.iid, image.extension)