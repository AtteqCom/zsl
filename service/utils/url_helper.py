'''
Created on 21.01.2013

@author: Peter Morihladko
'''

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    Drsny copy-paste z Djanga
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return mark_safe(re.sub('[-\s]+', '-', value))


def club(club):
    return '/sportove-kluby/{id}/{name}'.format(id=club.id, name=club.url)
