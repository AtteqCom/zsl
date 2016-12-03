'''
Modul na ulahcenie prace s redisom

.. moduleauthor::  Peter Morihladko
'''

from functools import partial
from zsl.utils.injection_helper import inject
from flask.config import Config


def redis_key(*args):
    return ':'.join(map(str, filter(lambda a: a is not None, args)))

class Keymaker(object):
    """
    Helper pre vytvaranie klucov k redisu v tvare 'sportky:daco:este:nieco..'
    Priklad:
        rkey = Keymaker(prefix='livescore', keys={'metoda': 'kluc', 'event': 'event', 'fav_event': 'favourite_event'}
        rkey.fav_event('user', 'sport', 'day') -> 'sportky:favourite_event:user:sport:day'
    """
    @inject(config=Config)
    def __init__(self, keys, prefix=None, config=None):
        project_specific_prefix = config.get('REDIS', {}).get('prefix')

        for method, key in keys.items():
            setattr(self, method, partial(redis_key, project_specific_prefix, prefix, key))
