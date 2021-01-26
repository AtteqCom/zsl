"""
:mod:`zsl.utils.redis_helper`
-----------------------------

Helper module for working with redis.

.. moduleauthor::  Peter Morihladko
"""
from functools import partial
from typing import Dict, Optional

from future.utils import viewitems
from injector import noninjectable

from zsl import Config, inject


def redis_key(*args):
    """Create a string key from a hierarchical structure.

    :param args: list of keys to denote hierarchy
    :type args: list(str)
    :return: string representation of args
    :rtype: str

    :Example:
        >>> redis_key(['project', 'module', 'class'])
        'project:module:class'
    """
    # TODO why there's `is not None`
    return ':'.join(str(a) for a in args if a is not None)


class Keymaker:
    """Keymaker is a class to generate an object to generate Redis keys.

    :Example:
        >>> article_keys = Keymaker(prefix='articles', keys={'full_article': 'full', 'short_article': 'short'})
        >>> article_keys.full_article('today', 'ID214')
        '$PROJECT_PREFIX:articles:full:today:ID214'
    """

    # TODO I think this should be done in proper OOP

    @inject
    @noninjectable('keys', 'prefix')
    def __init__(self, keys: Dict[str, str], prefix: Optional[str] = None, config: Config = None) -> None:
        project_specific_prefix = config.get('REDIS', {}).get('prefix')
        for method, key in viewitems(keys):
            setattr(self, method, partial(redis_key, project_specific_prefix, prefix, key))
