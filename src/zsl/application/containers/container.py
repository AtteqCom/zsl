"""
:mod:`zsl.application.containers.container`
-------------------------------------------
"""
from __future__ import unicode_literals

import inspect


class IoCContainer(object):
    """Collection of DI modules set as class attributes.

    This is used for declarative DI configuration, which can be easily
    extended upon.

    >>> class MyContainer(IoCContainer):
    ...   cache = MyCacheModule
    ...   redis = MyRedisModule

    >>> class MyTestContainer(MyContainer):
    ...   redis = MockRedisModule
    """
    @classmethod
    def modules(cls):
        """Collect all the public class attributes.

        All class attributes should be a DI modules, this method collects them
        and returns as a list.

        :return: list of DI modules
        :rtype: list[Union[Module, Callable]]
        """
        members = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a) and a.__name__ == 'modules'))
        modules = [module for name, module in members if not name.startswith('_')]
        return modules
