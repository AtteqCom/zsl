'''
Modul na ulahcenie prace s redisom 

@author Peter Morihladko
'''

from functools import partial


def redis_key(*args):
    return 'sportky:' + ':'.join(args);

class Keymaker:
    '''
    Helper pre vytvaranie klucov k redisu v tvare 'sportky:daco:este:nieco..'
    Priklad:
        rkey = Keymaker(prefix='livescore', keys={'metoda': 'kluc', 'event': 'event', 'fav_event': 'favourite_event'}
        rkey.fav_event('user', 'sport', 'day') -> 'sportky:favourite_event:user:sport:day'
    '''
    def __init__(self, keys, prefix=None):
        if prefix is None:
            prefix  = ''
        else:
            prefix = prefix + ':'

        for method,key in keys.items():
            setattr(self, method, partial(redis_key, prefix + key))
