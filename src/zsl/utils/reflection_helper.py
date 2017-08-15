"""
:mod:`zsl.utils.reflection_helper`
----------------------------------

Helper module for OOP operations.

.. moduleauthor:: Martin Babka
"""
from __future__ import absolute_import, division, print_function, unicode_literals

oldstr = str
from builtins import *  # NOQA


def extend(instance, new_class):
    """Adds new_class to the ancestors of instance.

    :param instance: Instance that will have a new ancestor.
    :param new_class: Ancestor.
    """
    instance.__class__ = type(
        '%s_extended_with_%s' % (instance.__class__.__name__, new_class.__name__),
        (new_class, instance.__class__,),
        {}
    )


def add_mixin(base_class, mixin_class):
    base_class.__bases__ = (mixin_class,) + base_class.__bases__
    return base_class


def is_scalar(v):
    return isinstance(v, (type(None), str, int, float, bool))


def proxy_object_to_delegate(proxy_object, delegate_object):
    proxy_class_name = 'Proxy{0}To{1}'.format(
        proxy_object.__class__.__name__,
        delegate_object.__class__.__name__)
    proxy_object.__class__ = type(oldstr(proxy_class_name),
                                  proxy_object.__class__.__bases__,
                                  dict(proxy_object.__class__.__dict__))
    proxy_object.__class__.__bases__ = (delegate_object.__class__,)
    proxy_object._delegate_object = delegate_object

    def __getattr__(self, item):
        return getattr(self._delegate_object, item)

    proxy_object.__class__.__getattr__ = __getattr__
